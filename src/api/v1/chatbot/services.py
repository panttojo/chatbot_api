from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.exceptions import NotFoundException
from core.bots.openai import OpenAIBot
from db.postgres.storage import PostgresStorage
from models.chatbot import Conversation, Message, RoleEnum

from .schemas import CreateMessageSchema


class ChatbotService:
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.storage = PostgresStorage(self.session)
        self.bot = OpenAIBot()

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

    async def save_message(self, conversation: Conversation, message: Message) -> None:
        logger.debug(f"Saving message: {message}")
        await self.storage.save(message)
        await self.storage.refresh(conversation, ["messages"])

    def get_previous_response_id(self, messages: list[Message]) -> str | None:
        bot_messages = [message for message in messages if message.role == RoleEnum.BOT]
        if bot_messages:
            return bot_messages[-1].extra_data["id"]
        return None

    async def handle_message(self, payload: CreateMessageSchema) -> Conversation:
        conversation = await self.retrieve_conversation(payload.conversation_id)
        conversation_id = conversation.id

        user_message = Message(conversation_id=conversation_id, message=payload.message, role=RoleEnum.USER)
        await self.save_message(conversation, user_message)
        previous_response_id = self.get_previous_response_id(conversation.messages)

        bot_response = self.bot.chat(
            message=payload.message,
            previous_response_id=previous_response_id,
            prompt_cache_key=str(conversation_id),
        )

        bot_message = Message(
            conversation_id=conversation_id,
            message=bot_response.output_text,
            role=RoleEnum.BOT,
            extra_data=bot_response.model_dump(mode="json"),
        )
        await self.save_message(conversation, bot_message)
        return conversation
