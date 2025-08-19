from sqlalchemy import UUID, Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel
from .enums import RoleEnum


class Conversation(BaseModel):
    __tablename__ = "conversations"

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation")


class Message(BaseModel):
    __tablename__ = "messages"

    conversation_id: UUID = Column(
        ForeignKey(Conversation.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True
    )
    role: RoleEnum = Column(Enum(RoleEnum), nullable=False)
    message: str = Column(String(255), nullable=False)

    conversation: Mapped[Conversation] = relationship("Conversation", back_populates="messages")
