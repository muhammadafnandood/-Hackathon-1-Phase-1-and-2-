"""
Configuration management for the Physical AI Textbook API.
Uses pydantic-settings for environment variable validation.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Physical AI Textbook API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    
    # BetterAuth
    BETTER_AUTH_SECRET: str
    BETTER_AUTH_URL: str = "http://localhost:8000"
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"
    OPENAI_LLM_MODEL: str = "gpt-4-turbo"
    OPENAI_MAX_TOKENS: int = 2000
    
    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "physical-ai-textbook"
    QDRANT_VECTOR_SIZE: int = 3072  # text-embedding-3-large
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return not self.DEBUG


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance."""
    global settings
    if settings is None:
        settings = Settings()
    return settings
