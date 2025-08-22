from loguru import logger
from openai import APITimeoutError, AsyncOpenAI, AuthenticationError, RateLimitError
from openai.types.conversations import Conversation
from openai.types.responses import Response

from core.bots.base import BaseBot
from core.settings import settings

from .schemas import ChatErrorResponse


class OpenAIBot(BaseBot):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.LLM_API_KEY.get_secret_value())

    async def create_conversation(self) -> Conversation:
        """
        Create a new conversation with the OpenAI API.

        Returns:
            The created conversation.
        """
        return await self.client.conversations.create()

    async def chat(
        self,
        message: str,
        conversation_id: str | None = None,
        prompt_cache_key: str | None = None,
        chat_model: str = settings.LLM_MODEL,
        reasoning: dict = settings.LLM_REASONING,
    ) -> Response:
        """
        Send a message to the OpenAI API and receive a response.

        Args:
            message: The message to send to the OpenAI API.
            conversation_id: The ID of the conversation to send the message to.
            prompt_cache_key: The key to use for caching the prompt.
            chat_model: The model to use for the chat.
            reasoning: The reasoning to use for the chat.

        Returns:
            The response from the OpenAI API.
        """
        prompt = self.prompt

        input_data = [{"role": "user", "content": message}]

        try:
            response = await self.client.responses.create(
                model=chat_model,
                reasoning=reasoning,
                instructions=prompt,
                input=input_data,
                prompt_cache_key=prompt_cache_key,
                conversation=conversation_id,
                store=True,
            )

            logger.success(f"Response: {response}")
        except AuthenticationError as error:
            logger.error(f"Error: {error}")
            response = ChatErrorResponse(output_text="Ocurrió un error, por favor contacta al administrador.")
        except (RateLimitError, APITimeoutError) as error:
            logger.error(f"Error: {error}")
            response = ChatErrorResponse(output_text="Ocurrió un error, por favor intenta más tarde.")
        except Exception as error:  # noqa: BLE001
            logger.exception(error)
            response = ChatErrorResponse(output_text=str(error))

        return response
