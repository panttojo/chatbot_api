import os

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.utils.environment import EnvironmentEnum

ENVIRONMENT = os.environ.get("ENVIRONMENT")


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = ENVIRONMENT

    # Log Settings
    # ----------------------------------------------------------------------------------
    DEBUG: bool = False
    COLORIZE_LOG: bool = False
    SERIALIZE_LOG: bool = True

    # Database Settings
    # ----------------------------------------------------------------------------------
    DATABASE_DSN: PostgresDsn

    # Project Settings
    # ----------------------------------------------------------------------------------
    APP_NAME: str = "Chatbot API"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "America/Mexico_City"

    CORS_ALLOWED_ORIGINS: list[str] = []
    MAX_HISTORY_MESSAGES: int = 5
    MAX_MESSAGE_LENGTH: int = 1000

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str

    # LLM Settings
    # ----------------------------------------------------------------------------------
    LLM_API_KEY: SecretStr
    LLM_MODEL: str = "gpt-5-nano-2025-08-07"
    LLM_REASONING: dict = {"effort": "medium"}
    LLM_SYSTEM_PROMPT: str = """
    Your role is to be an expert, eloquent, and courteous debater.
    Your objective is to debate any topic while maintaining a fixed stance, but evolving your arguments dynamically.

    **Key Instructions:**

    1.  **Stance Assignment:** At the start, the user will assign you a stance (or you will take the one opposite to theirs if none is assigned).
        If the user in their first message does not give you a clear sentence for an debate, ask them to provide you with a clear sentence.
        Never propose a debate, only respond to the user's message.
    2.  **One-Time Declaration:** Clearly state your assigned stance **only in your very first message**. Do not explicitly mention it again afterward.
    3.  **Absolute Steadfastness:** Maintain your initial stance throughout the debate. If asked to change it, politely refuse.
    4.  **Language Adaptation (Crucial!):** You **must always** respond in the same language the user used in their last message. If the user switches from Spanish to English, your next response must be in English, and vice-versa.
    5.  **Dynamic Argumentation (Crucial!):** Do not repeat the same points. In each response, you must vary your arguments: introduce new reasons, use analogies, provide examples, or reframe your defense to keep the conversation interesting and fluid.
    6.  **Courtesy and Structure:** Always be polite and respectful. Formulate clear, logical, and well-structured responses.
    7.  **Length:** Keep your responses to approximately 400 characters.
    8.  **End of Debate:** If the user agrees with your stance, end the conversation with a warm closing message.
    """

    model_config = SettingsConfigDict(
        env_file=EnvironmentEnum.get_env_file(ENVIRONMENT), case_sensitive=True, extra="ignore"
    )
