"""
RAG API for Physical AI Textbook
FastAPI-based chatbot with vector search over textbook content
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import local modules
from database import get_db_session, DatabaseSession
from embeddings import EmbeddingService
from qdrant_client import QdrantClient
from chat import ChatService

# ============================================
# Lifespan
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    app.state.db = get_db_session()
    app.state.embedding_service = EmbeddingService(
        model_name=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    )
    app.state.qdrant = QdrantClient(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    app.state.chat_service = ChatService(
        db=app.state.db,
        qdrant=app.state.qdrant,
        embedding_service=app.state.embedding_service,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    print("✅ RAG API started successfully")
    
    yield
    
    # Shutdown
    app.state.db.close()
    print("👋 RAG API shutdown complete")


# ============================================
# App Initialization
# ============================================

app = FastAPI(
    title="Physical AI Textbook RAG API",
    description="AI-powered chatbot for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Pydantic Models
# ============================================

class ChatMessage(BaseModel):
    """Chat message request."""
    message: str = Field(..., description="User's question or message")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    top_k: int = Field(3, description="Number of chunks to retrieve")
    
class ChatResponse(BaseModel):
    """Chat response."""
    response: str
    sources: List[Dict[str, Any]]
    session_id: str
    model: str
    
class ChunkRequest(BaseModel):
    """Request to add chunks for embedding."""
    chapter_id: str
    content: str
    heading: Optional[str] = None
    
class SearchRequest(BaseModel):
    """Vector search request."""
    query: str
    top_k: int = 5
    chapter_id: Optional[str] = None


# ============================================
# Health Endpoints
# ============================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Physical AI Textbook RAG API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "qdrant": "connected"
    }


# ============================================
# Chat Endpoints
# ============================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """
    Chat with the AI textbook assistant.
    
    The AI will:
    1. Embed the user's question
    2. Search for relevant textbook chunks
    3. Generate a response using LLM with retrieved context
    4. Return response with sources
    """
    try:
        response = await app.state.chat_service.chat(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            top_k=request.top_k
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/sessions")
async def create_chat_session(user_id: Optional[str] = None):
    """Create a new chat session."""
    session = await app.state.chat_service.create_session(user_id)
    return session


@app.get("/chat/sessions/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session history."""
    messages = await app.state.chat_service.get_session_history(session_id)
    return {"session_id": session_id, "messages": messages}


# ============================================
# Embedding Endpoints
# ============================================

@app.post("/embeddings/chunks")
async def add_chunk(request: ChunkRequest):
    """Add a text chunk for embedding and vector search."""
    try:
        result = await app.state.chat_service.add_chunk(
            chapter_id=request.chapter_id,
            content=request.content,
            heading=request.heading
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embeddings/batch")
async def add_chunks_batch(chapters: List[ChunkRequest]):
    """Add multiple chunks in batch."""
    results = []
    for chapter in chapters:
        try:
            result = await app.state.chat_service.add_chunk(
                chapter_id=chapter.chapter_id,
                content=chapter.content,
                heading=chapter.heading
            )
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})
    return {"results": results}


# ============================================
# Search Endpoints
# ============================================

@app.post("/search")
async def search(request: SearchRequest):
    """
    Search textbook content using vector similarity.
    
    Returns relevant chunks ranked by similarity.
    """
    try:
        results = await app.state.chat_service.search(
            query=request.query,
            top_k=request.top_k,
            chapter_id=request.chapter_id
        )
        return {"query": request.query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Personalization Endpoints
# ============================================

@app.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile for personalization."""
    profile = await app.state.chat_service.get_user_profile(user_id)
    return profile


@app.put("/users/{user_id}/profile")
async def update_user_profile(user_id: str, profile: Dict[str, Any]):
    """Update user profile for personalization."""
    updated = await app.state.chat_service.update_user_profile(user_id, profile)
    return updated


@app.get("/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get user's learning progress."""
    progress = await app.state.chat_service.get_user_progress(user_id)
    return progress


# ============================================
# Analytics Endpoints
# ============================================

@app.post("/analytics/events")
async def track_event(event_type: str, event_data: Dict[str, Any], user_id: Optional[str] = None):
    """Track analytics event."""
    await app.state.chat_service.track_event(event_type, event_data, user_id)
    return {"status": "tracked"}


# ============================================
# Main
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
