from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError

from core.settings import settings
from models.enums import RoleEnum


# Message Schemas
# -----------------------------------------------------------------------------
class MessageSchema(BaseModel):
    role: RoleEnum
    message: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CreateMessageSchema(BaseModel):
    message: str
    conversation_id: UUID | None = None

    @field_validator("message", mode="before")
    @classmethod
    def validate_message_length(cls, message: str) -> str:
        if len(message) > settings.MAX_MESSAGE_LENGTH:
            msg = "value_error"
            raise PydanticCustomError(
                msg,
                "Message length must be less than 1000 characters",
            )
        return message


# Conversation Schemas
# -----------------------------------------------------------------------------
class ConversationSchema(BaseModel):
    id: UUID = Field(serialization_alias="conversation_id")
    messages: list[MessageSchema] | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
