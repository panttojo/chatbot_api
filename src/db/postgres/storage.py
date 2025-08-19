from typing import TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class PostgresStorage:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, instance: T, refresh_attributes: list[str] | None = None) -> T:
        if refresh_attributes is None:
            refresh_attributes = []

        self.session.add(instance)
        await self.session.flush()
        await self.refresh(instance, refresh_attributes)
        return instance

    async def retrieve(self, model: T, key: UUID | str) -> T | None:
        return await self.session.get(model, key)

    async def refresh(self, instance: T, refresh_attributes: list[str] | None = None) -> T:
        if refresh_attributes is None:
            refresh_attributes = []
        await self.session.refresh(instance, refresh_attributes)
        return instance
