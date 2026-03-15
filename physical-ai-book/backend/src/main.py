"""
Physical AI Textbook API - FastAPI Main Application

This is the main entry point for the backend API that provides:
- Authentication via BetterAuth
- RAG-powered chatbot for textbook Q&A
- Personalization engine for adaptive learning
- Urdu translation services
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.utils.logger import setup_logger

# Import API routers (to be implemented)
# from src.api import chat, translate, personalize, users, auth

# Configure logging
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting Physical AI Textbook API...")
    settings = get_settings()
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database configured: {'✓' if settings.DATABASE_URL else '✗'}")
    logger.info(f"Qdrant configured: {'✓' if settings.QDRANT_URL else '✗'}")
    logger.info(f"OpenAI configured: {'✓' if settings.OPENAI_API_KEY else '✗'}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Physical AI Textbook API...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-native textbook platform API with RAG chatbot, personalization, and Urdu translation",
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routers (to be implemented in later tasks)
    # app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    # app.include_router(users.router, prefix="/api/users", tags=["User Profile"])
    # app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
    # app.include_router(personalize.router, prefix="/api/chapters", tags=["Personalization"])
    # app.include_router(translate.router, prefix="/api/translate", tags=["Translation"])
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
        }
    
    logger.info("Application created successfully")
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
