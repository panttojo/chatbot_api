from loguru import logger
from openai import APITimeoutError, AuthenticationError, OpenAI, RateLimitError
from openai.types.responses import Response

from core.bots.base import BaseBot
from core.settings import settings

from .schemas import ChatErrorResponse


class OpenAIBot(BaseBot):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.LLM_API_KEY.get_secret_value())

    def chat(
        self,
        message: str,
        previous_response_id: str | None = None,
        prompt_cache_key: str | None = None,
        chat_model: str = settings.LLM_MODEL,
        reasoning: dict = settings.LLM_REASONING,
    ) -> Response:
        prompt = self.prompt

        input_data = [{"role": "user", "content": message}]

        try:
            response = self.client.responses.create(
                model=chat_model,
                reasoning=reasoning,
                instructions=prompt,
                input=input_data,
                prompt_cache_key=prompt_cache_key,
                previous_response_id=previous_response_id,
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
