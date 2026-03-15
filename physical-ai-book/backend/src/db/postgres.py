"""
Database configuration and session management.
Uses SQLAlchemy with async support for PostgreSQL.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import get_settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_engine():
    """Create and return async SQLAlchemy engine."""
    settings = get_settings()
    
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,  # SQL logging in debug mode
        pool_pre_ping=True,  # Enable connection health checks
        pool_size=10,
        max_overflow=20,
    )
    
    return engine


def get_session_maker():
    """Create and return async session maker."""
    engine = get_engine()
    
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session.
    Yields an async session and ensures proper cleanup.
    """
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    engine = get_engine()
    
    # Import all models to ensure they're registered with Base
    from src.models import user, chat, personalized_content, translation
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    engine = get_engine()
    await engine.dispose()
