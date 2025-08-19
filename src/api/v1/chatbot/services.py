from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.exceptions import NotFoundException
from db.postgres.storage import PostgresStorage
from models.chatbot import Conversation, Message, RoleEnum

from .schemas import CreateMessageSchema


class ChatbotService:
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.storage = PostgresStorage(self.session)

    async def retrieve_conversation(self, conversation_id: UUID | None) -> Conversation:
        if conversation_id is None:
            conversation = await self.storage.save(Conversation())
            logger.success(f"Conversation created: {conversation}")
        else:
            conversation = await self.storage.retrieve(Conversation, conversation_id)
            logger.debug(f"Conversation found: {conversation}")
            if not conversation:
                raise NotFoundException(detail="Conversation not found")

        return conversation

    async def handle_message(self, payload: CreateMessageSchema, max_messages: int = 5) -> Conversation:
        conversation = await self.retrieve_conversation(payload.conversation_id)
        message = Message(conversation_id=conversation.id, message=payload.message, role=RoleEnum.USER)
        await self.storage.save(message)
        await self.storage.refresh(conversation, ["messages"])
        conversation.messages = conversation.messages[-max_messages:]
        return conversation
