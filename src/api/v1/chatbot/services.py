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
        """
        Retrieve a conversation from the database or create a new one if it doesn't exist.

        Args:
            conversation_id: The ID of the conversation to retrieve.

        Returns:
            The retrieved conversation.

        Raises:
            NotFoundException: If the conversation is not found.
        """
        if conversation_id is None:
            llm_conversation = await self.bot.create_conversation()
            conversation = await self.storage.save(Conversation(external_id=llm_conversation.id))
            logger.success(f"Conversation created: {conversation}")
        else:
            conversation = await self.storage.retrieve(Conversation, conversation_id)
            logger.debug(f"Conversation found: {conversation}")
            if not conversation:
                raise NotFoundException(detail="Conversation not found")

        return conversation

    async def save_message(self, conversation: Conversation, message: Message) -> None:
        """
        Save a message to the database.

        Args:
            conversation: The conversation to save the message to.
            message: The message to save.
        """
        logger.debug(f"Saving message: {message}")
        await self.storage.save(message)
        await self.storage.refresh(conversation, ["messages"])

    def get_previous_response_id(self, messages: list[Message]) -> str | None:
        bot_messages = [
            message for message in messages if message.role == RoleEnum.BOT and message.extra_data.get("id")
        ]
        if bot_messages:
            return bot_messages[-1].extra_data.get("id")
        return None

    async def handle_message(self, payload: CreateMessageSchema) -> Conversation:
        """
        Handle a message from the user.

        Args:
            payload: The payload containing the message and conversation ID.

        Returns:
            The conversation with the new message.
        """
        conversation = await self.retrieve_conversation(payload.conversation_id)
        conversation_id = conversation.id

        user_message = Message(conversation_id=conversation_id, message=payload.message, role=RoleEnum.USER)
        await self.save_message(conversation, user_message)

        bot_response = await self.bot.chat(
            message=payload.message,
            conversation_id=conversation.external_id,
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
