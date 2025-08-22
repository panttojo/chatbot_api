from fastapi import APIRouter, status
from loguru import logger

from core.settings import settings
from db.postgres.session import DBSession

from .schemas import ConversationSchema, CreateMessageSchema
from .services import ChatbotService

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def chat(payload: CreateMessageSchema, session: DBSession) -> ConversationSchema:
    """
    Handle a message from the user.

    Args:
        payload: The payload containing the message and conversation ID.
        session: The database session.

    Returns:
        The conversation with the new message.
    """
    conversation = await ChatbotService(session=session).handle_message(payload=payload)
    response = ConversationSchema.model_validate(conversation)
    response.messages = response.messages[-settings.MAX_HISTORY_MESSAGES :]
    logger.success(f"Response: {response}")
    return response
