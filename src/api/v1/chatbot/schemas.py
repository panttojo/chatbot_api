from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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


# Conversation Schemas
# -----------------------------------------------------------------------------
class ConversationSchema(BaseModel):
    id: UUID = Field(serialization_alias="conversation_id")
    messages: list[MessageSchema] | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
