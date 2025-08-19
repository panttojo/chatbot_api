from fastapi import APIRouter, status
from loguru import logger

from db.postgres.session import DBSession

from .schemas import ConversationSchema, CreateMessageSchema
from .services import ChatbotService

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(payload: CreateMessageSchema, session: DBSession) -> ConversationSchema:
    conversation = await ChatbotService(session=session).handle_message(payload=payload)
    response = ConversationSchema.model_validate(conversation).model_dump(mode="json")
    logger.success(f"Response: {response}")
    return response
