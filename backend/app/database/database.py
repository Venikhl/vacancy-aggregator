"""Database configuration."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.core.config import get_settings


engine = create_async_engine(get_settings().DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession,
                                   expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async context manager for database sessions."""
    async with async_session_maker() as session:
        yield session
