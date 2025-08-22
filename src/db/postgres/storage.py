from typing import TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class PostgresStorage:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, instance: T, refresh_attributes: list[str] | None = None) -> T:
        """
        Save a model instance to the database.

        Args:
            instance: The model instance to save.
            refresh_attributes: A list of attributes to refresh after saving.

        Returns:
            The saved model instance.

        Raises:
            SQLAlchemyError: If there is an error saving the model instance.
        """
        if refresh_attributes is None:
            refresh_attributes = []

        self.session.add(instance)
        await self.session.flush()
        await self.refresh(instance, refresh_attributes)
        return instance

    async def retrieve(self, model: T, key: UUID | str) -> T | None:
        """
        Retrieve a model instance from the database.

        Args:
            model: The model class to retrieve.
            key: The key of the model instance to retrieve.

        Returns:
            The retrieved model instance.

        Raises:
            SQLAlchemyError: If there is an error retrieving the model instance.
        """
        return await self.session.get(model, key)

    async def refresh(self, instance: T, refresh_attributes: list[str] | None = None) -> T:
        """
        Refresh a model instance from the database.

        Args:
            instance: The model instance to refresh.
            refresh_attributes: A list of attributes to refresh.

        Returns:
            The refreshed model instance.

        Raises:
            SQLAlchemyError: If there is an error refreshing the model instance.
        """
        if refresh_attributes is None:
            refresh_attributes = []
        await self.session.refresh(instance, refresh_attributes)
        return instance
