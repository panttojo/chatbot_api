from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from core.settings import settings

APPLICATION_NAME = settings.APP_NAME.replace(" ", "-").lower()


async_engine = create_async_engine(
    settings.DATABASE_DSN.unicode_string(),
    connect_args={"application_name": APPLICATION_NAME},
)


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
