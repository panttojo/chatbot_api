from abc import ABC, abstractmethod

from models.base import BaseModel


class BaseStorage(ABC):
    @abstractmethod
    async def save(self, instance: BaseModel, refresh_attributes: list[str] | None = None) -> BaseModel: ...

    @abstractmethod
    async def retrieve(self, model: type[BaseModel], key: str) -> BaseModel | None: ...

    @abstractmethod
    async def refresh(self, instance: BaseModel, refresh_attributes: list[str] | None = None) -> BaseModel: ...
