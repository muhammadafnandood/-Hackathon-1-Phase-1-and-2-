"""
RAG Chatbot FastAPI Server - Simple Version

Uses SQLite-based vector store for local development.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import dotenv

from simple_ingest import SimpleVectorStore

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


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: List[Dict[str, Any]] = []
    confidence: float
    query: str
    chunks_retrieved: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    vector_store_connected: bool
    collection_name: str
    vector_count: Optional[int] = None


# ============== Application Lifecycle ==============

vector_store: Optional[SimpleVectorStore] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global vector_store

    # Startup
    logger.info("Starting RAG Chatbot server...")

    try:
        db_path = Path(__file__).parent / "vector_store.db"
        vector_store = SimpleVectorStore(str(db_path))
        logger.info(f"✓ Vector store initialized: {db_path}")
    except Exception as e:
        logger.error(f"⚠ Failed to initialize vector store: {e}")
        vector_store = None

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot server...")
    if vector_store:
        vector_store.close()


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Helper Functions ==============

def generate_answer(query: str, context: str) -> str:
    """Generate answer based on context using simple template."""
    
    if not context:
        return "I don't have specific information about that topic in the textbook. Please try rephrasing your question or ask about Physical AI, humanoid robotics, ROS 2, sensors, motion planning, machine learning for robotics, VLA models, digital twins, or system integration."
    
    prompt = f"""Based on the following textbook content, answer the question concisely and clearly.

TEXTBOOK CONTENT:
{context}

QUESTION: {query}

ANSWER: """

    # Simple template-based answer generation
    # In production, this would call OpenAI or another LLM
    answer = f"Based on the textbook content:\n\n{context}\n\nThis addresses your question about '{query}'."
    
    return answer


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
            "health": "GET /health",
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Get an answer to a question based on textbook content.
    """
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    try:
        logger.info(f"Processing query: {request.query[:100]}...")

        # Search for relevant chunks
        results = vector_store.search(request.query, top_k=request.top_k)

        if not results:
            return ChatResponse(
                answer="I couldn't find relevant information about that topic in the textbook. Please try rephrasing your question.",
                sources=[],
                confidence=0.0,
                query=request.query,
                chunks_retrieved=0
            )

        # Format context
        context_parts = []
        sources = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result['chapter_title']} - {result['section_name']}]\n"
                f"{result['text']}\n"
            )
            sources.append({
                "chapter": result["chapter_title"],
                "section": result["section_name"],
                "url": result["page_url"],
                "score": result["score"],
            })

        context = "\n---\n".join(context_parts)

        # Generate answer
        answer = generate_answer(request.query, context)

        # Calculate confidence
        confidence = sum(r["score"] for r in results) / len(results) if results else 0.0

        logger.info(f"Query processed successfully. Confidence: {confidence:.2f}")

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=round(confidence, 2),
            query=request.query,
            chunks_retrieved=len(results)
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health of service components."""
    if vector_store is None:
        return HealthResponse(
            status="unhealthy",
            vector_store_connected=False,
            collection_name="",
        )

    try:
        stats = vector_store.get_stats()
        
        return HealthResponse(
            status="healthy",
            vector_store_connected=True,
            collection_name=stats.get("collection_name", ""),
            vector_count=stats.get("vector_count", 0),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="degraded",
            vector_store_connected=True,
            collection_name="",
        )


@app.get("/sources")
async def get_sources(query: str, top_k: int = 5):
    """Get source information for a query."""
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    try:
        results = vector_store.search(query, top_k=top_k)

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
        "main_simple:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
