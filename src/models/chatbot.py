from uuid import UUID

from sqlalchemy import JSON, Enum, Text
from sqlmodel import Field, Relationship

from .base import BaseModel
from .enums import RoleEnum


class Message(BaseModel, table=True):
    role: RoleEnum = Field(sa_type=Enum(RoleEnum))
    message: str = Field(sa_type=Text)
    extra_data: dict | None = Field(default=None, sa_type=JSON)

    conversation_id: UUID = Field(foreign_key="conversation.id")
    conversation: "Conversation" = Relationship(back_populates="messages")


class Conversation(BaseModel, table=True):
    messages: list["Message"] = Relationship(
        back_populates="conversation", sa_relationship_kwargs={"order_by": Message.created_at}
    )
