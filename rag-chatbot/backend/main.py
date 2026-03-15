"""
RAG Chatbot FastAPI Server

Provides REST API endpoints for the textbook Q&A chatbot.

Endpoints:
    POST /chat - Get answer to a question
    POST /chat/stream - Stream answer in real-time
    GET /health - Health check
    GET /sources - Get sources for a query
    POST /feedback - Submit feedback on an answer
"""

import os
import logging
from typing import List, Optional, Dict, Any
from datetime import timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
import uvicorn
import dotenv

from rag_pipeline import RAGPipeline, ChatResponse, StreamChunk
from vector_store import get_qdrant_client
from personalizer import UserProfile, ExperienceLevel
from auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    MessageResponse,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from database import User, get_db_session
from sqlalchemy.orm import Session
from urdu_translator import translate_to_urdu as translate_text

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============== Request/Response Models ==============

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="User's question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    include_sources: bool = Field(default=True, description="Whether to include sources")
    use_mmr: bool = Field(default=True, description="Use Maximal Marginal Relevance")
    
    # User profile for personalization
    programming_experience: Optional[str] = Field(None, description="User's programming level")
    robotics_knowledge: Optional[str] = Field(None, description="User's robotics knowledge")
    ai_experience: Optional[str] = Field(None, description="User's AI/ML experience")
    hardware_experience: Optional[str] = Field(None, description="User's hardware experience")
    
    def get_user_profile(self) -> Optional[UserProfile]:
        """Build UserProfile from request fields if any are provided."""
        # Check if any profile field is provided
        if not any([
            self.programming_experience,
            self.robotics_knowledge,
            self.ai_experience,
            self.hardware_experience,
        ]):
            return None
        
        # Map string values to ExperienceLevel enum
        def to_level(value: Optional[str]) -> ExperienceLevel:
            if not value:
                return ExperienceLevel.BEGINNER  # Default to beginner if not specified
            try:
                return ExperienceLevel(value.lower())
            except ValueError:
                return ExperienceLevel.BEGINNER
        
        return UserProfile(
            programming_experience=to_level(self.programming_experience),
            robotics_knowledge=to_level(self.robotics_knowledge),
            ai_experience=to_level(self.ai_experience),
            hardware_experience=to_level(self.hardware_experience),
        )


class ChatResponseModel(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: List[Dict[str, Any]] = []
    confidence: float
    query: str
    model_used: str
    chunks_retrieved: int
    user_profile: Optional[Dict[str, str]] = None
    personalization_applied: bool = False


class StreamResponseModel(BaseModel):
    """Model for streamed response chunks."""
    content: str
    is_final: bool
    sources: Optional[List[Dict[str, Any]]] = None
    confidence: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    qdrant_connected: bool
    openai_connected: bool
    collection_name: str
    vector_count: Optional[int] = None


class FeedbackRequest(BaseModel):
    """Feedback submission model."""
    query: str
    answer: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 (bad) to 5 (excellent)")
    feedback_text: Optional[str] = None


class UserProfileRequest(BaseModel):
    """User profile creation model."""
    programming_experience: str = Field(..., description="beginner, intermediate, or advanced")
    robotics_knowledge: str = Field(..., description="beginner, intermediate, or advanced")
    ai_experience: str = Field(..., description="beginner, intermediate, or advanced")
    hardware_experience: str = Field(..., description="beginner, intermediate, or advanced")
    learning_style: Optional[str] = Field("balanced", description="visual, hands-on, theoretical, or balanced")
    goals: Optional[str] = None


class UserProfileResponse(BaseModel):
    """User profile response model."""
    profile: Dict[str, str]
    overall_level: str
    recommendations: List[str]


# ============== Application Lifecycle ==============

# Global pipeline instance
pipeline: Optional[RAGPipeline] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global pipeline

    # Startup
    logger.info("Starting RAG Chatbot server...")

    try:
        collection_name = os.getenv("RAG_COLLECTION", "textbook_knowledge")
        pipeline = RAGPipeline(collection_name=collection_name)
        logger.info(f"✓ RAG Pipeline initialized with collection: {collection_name}")
    except Exception as e:
        logger.error(f"⚠ Failed to initialize RAG pipeline: {e}")
        logger.warning("Server will run in limited mode (Qdrant not connected)")
        pipeline = None

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot server...")
    if pipeline and hasattr(pipeline.qdrant_client, 'close'):
        pipeline.qdrant_client.close()


# ============== FastAPI App ==============

app = FastAPI(
    title="RAG Textbook Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Docusaurus dev server
        "http://localhost:8080",  # Alternative frontend
        "*",  # Allow all in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Endpoints ==============

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "RAG Textbook Chatbot API",
        "version": "1.0.0",
        "description": "Ask questions about Physical AI & Humanoid Robotics textbook",
        "endpoints": {
            "chat": "POST /chat",
            "stream": "POST /chat/stream",
            "health": "GET /health",
            "feedback": "POST /feedback",
        }
    }


@app.post("/chat", response_model=ChatResponseModel)
async def chat(request: ChatRequest):
    """
    Get an answer to a question based on textbook content.

    The chatbot retrieves relevant chunks from the textbook and generates
    an answer using OpenAI GPT.

    Optionally personalizes the response based on user's technical background.
    """
    if pipeline is None:
        # Return a friendly fallback response when Qdrant is not connected
        logger.warning("Qdrant not connected - using fallback response")
        return ChatResponseModel(
            answer=f"I understand you're asking about: '{request.query}'. \n\n⚠️ **Note:** The vector database (Qdrant) is not currently connected. To provide accurate textbook-based answers, please ensure:\n\n1. Qdrant server is running\n2. Vector database is populated with textbook content\n3. Check your `.env` file for correct Qdrant URL and API key\n\nOnce connected, I'll be able to give you detailed answers from the Physical AI & Humanoid Robotics textbook!",
            sources=[],
            confidence=0.0,
            query=request.query,
            model_used="fallback",
            chunks_retrieved=0,
            user_profile=None,
            personalization_applied=False,
        )
    
    try:
        logger.info(f"Processing query: {request.query[:100]}...")

        # Build user profile from request
        user_profile = request.get_user_profile()

        response = pipeline.query(
            question=request.query,
            top_k=request.top_k,
            use_mmr=request.use_mmr,
            user_profile=user_profile,
        )

        # Remove sources if not requested
        if not request.include_sources:
            response.sources = []

        logger.info(f"Query processed successfully. Confidence: {response.confidence}")
        if response.personalization_applied:
            logger.info(f"Personalization applied for level: {response.user_profile}")

        return ChatResponseModel(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence,
            query=response.query,
            model_used=response.model_used,
            chunks_retrieved=response.chunks_retrieved,
            user_profile=response.user_profile,
            personalization_applied=response.personalization_applied,
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream an answer to a question in real-time.
    
    Returns Server-Sent Events (SSE) stream for better UX.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    async def generate_stream():
        try:
            for chunk in pipeline.query_stream(
                question=request.query,
                top_k=request.top_k,
            ):
                # Format as SSE
                data = StreamResponseModel(
                    content=chunk.content,
                    is_final=chunk.is_final,
                    sources=chunk.sources,
                    confidence=chunk.confidence,
                )
                yield f"data: {data.json()}\n\n"
                
                if chunk.is_final:
                    break
                    
        except Exception as e:
            logger.error(f"Stream error: {e}")
            error_chunk = StreamResponseModel(
                content=f"Error: {str(e)}",
                is_final=True,
            )
            yield f"data: {error_chunk.json()}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health of all service components."""
    if pipeline is None:
        return HealthResponse(
            status="unhealthy",
            qdrant_connected=False,
            openai_connected=False,
            collection_name="",
        )
    
    try:
        health = pipeline.health_check()
        qdrant_stats = health.get("qdrant", {})
        
        return HealthResponse(
            status=health.get("status", "unknown"),
            qdrant_connected=qdrant_stats.get("connected", False),
            openai_connected=health.get("openai") == "connected",
            collection_name=health.get("collection", ""),
            vector_count=qdrant_stats.get("vector_count"),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            qdrant_connected=False,
            openai_connected=False,
            collection_name="",
        )


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest, background_tasks: BackgroundTasks):
    """
    Submit feedback on a chatbot answer.
    
    Feedback is logged for analytics and improvement.
    """
    # Log feedback (in production, store in database)
    feedback_data = {
        "timestamp": str(__import__("datetime").datetime.now()),
        "query": request.query,
        "answer": request.answer[:200],  # Truncate for logging
        "rating": request.rating,
        "feedback_text": request.feedback_text,
    }
    
    logger.info(f"Feedback received: {feedback_data}")
    
    # In production, save to database:
    # background_tasks.add_task(save_feedback_to_db, feedback_data)
    
    return {
        "status": "success",
        "message": "Thank you for your feedback!",
        "feedback_id": str(hash(str(feedback_data))),
    }


@app.post("/api/translate/urdu")
async def translate_to_urdu_endpoint(
    content: str = Field(..., min_length=1, max_length=5000),
    language: str = Field(default="urdu", description="Target language")
):
    """
    Translate text to Urdu.

    Translates technical content while preserving:
    - Technical terminology (ROS 2, AI, ML, etc.)
    - Code blocks
    - Markdown formatting
    """
    try:
        # Translate the content
        translated = translate_text(content)

        return {
            "translated": translated,
            "from_cache": False,
            "language": "urdu"
        }
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


@app.get("/sources")
async def get_sources(query: str, top_k: int = 5):
    """
    Get source information for a query without generating an answer.
    
    Useful for showing users where information comes from.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        # Embed and retrieve
        query_vector = pipeline.embed_query(query)
        results, _ = pipeline.retrieve_context(query_vector)
        
        sources = [
            {
                "chapter": r["chapter_title"],
                "section": r["section_name"],
                "url": r["page_url"],
                "score": r["score"],
                "preview": r["text"][:200] + "..." if len(r["text"]) > 200 else r["text"],
            }
            for r in results
        ]
        
        return {
            "query": query,
            "sources": sources,
            "total_found": len(sources),
        }
        
    except Exception as e:
        logger.error(f"Error getting sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profile/analyze")
async def analyze_user_profile(request: UserProfileRequest):
    """
    Analyze user profile and provide learning recommendations.
    
    This helps users understand their learning path and get personalized
    content recommendations.
    """
    def to_level(value: str) -> ExperienceLevel:
        try:
            return ExperienceLevel(value.lower())
        except ValueError:
            return ExperienceLevel.BEGINNER
    
    profile = UserProfile(
        programming_experience=to_level(request.programming_experience),
        robotics_knowledge=to_level(request.robotics_knowledge),
        ai_experience=to_level(request.ai_experience),
        hardware_experience=to_level(request.hardware_experience),
        learning_style=request.learning_style or "balanced",
        goals=request.goals,
    )
    
    overall_level = profile.get_overall_level()
    
    # Generate recommendations based on profile
    recommendations = []
    
    # Domain-specific recommendations
    if profile.programming_experience == ExperienceLevel.BEGINNER:
        recommendations.append("Start with Python basics before diving into ROS 2 nodes")
    if profile.robotics_knowledge == ExperienceLevel.BEGINNER:
        recommendations.append("Learn fundamental robotics concepts: sensors, actuators, control loops")
    if profile.ai_experience == ExperienceLevel.BEGINNER:
        recommendations.append("Begin with basic ML concepts before exploring VLA models")
    if profile.hardware_experience == ExperienceLevel.BEGINNER:
        recommendations.append("Focus on simulation first; hardware can be added later")
    
    # Level-based recommendations
    if overall_level == ExperienceLevel.BEGINNER:
        recommendations.extend([
            "Follow chapters in order - each builds on previous concepts",
            "Run all code examples yourself to build muscle memory",
            "Join the community forum to ask questions",
        ])
    elif overall_level == ExperienceLevel.INTERMEDIATE:
        recommendations.extend([
            "Focus on chapters outside your comfort zone",
            "Try the advanced exercises at the end of each chapter",
            "Consider contributing to open-source robotics projects",
        ])
    else:  # Advanced
        recommendations.extend([
            "Explore research papers linked in advanced sections",
            "Consider implementing algorithms from scratch",
            "Look into cutting-edge topics like VLA models and digital twins",
        ])
    
    return UserProfileResponse(
        profile=profile.to_dict(),
        overall_level=overall_level.value,
        recommendations=recommendations,
    )


# ============== Authentication Endpoints ==============

@app.post("/auth/register", response_model=MessageResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db_session)):
    """
    Register a new user account.

    Creates a new user with the provided email and password.
    Email must be unique.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {user_data.email}")

    return MessageResponse(message="Account created successfully! Please login.")


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    """
    Login and get access token.

    Returns a JWT token for authenticated user.
    """
    from fastapi import status

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(f"User logged in: {user.email}")

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
        ),
    )


@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information.

    Requires valid authentication token.
    """
    return current_user


# ============== Error Handlers ==============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP error: {exc.status_code} - {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled error: {exc}")
    return {
        "error": "Internal server error",
        "status_code": 500,
    }


# ============== Main ==============

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
