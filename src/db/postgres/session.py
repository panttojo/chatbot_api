from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from core.settings import settings
from models.chatbot import *  # noqa: F403

APPLICATION_NAME = settings.APP_NAME.replace(" ", "-").lower()


async_engine = create_async_engine(
    settings.DATABASE_DSN.unicode_string(),
    connect_args={"application_name": APPLICATION_NAME},
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def use_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.exception(e)
            raise


# Alias for using in FastAPI dependencies
DBSession = Annotated[AsyncSession, Depends(use_session)]


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def test_db_connection() -> bool | None:
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.success(f"Database connection successful: {result.scalar()}")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False
