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

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str

    # LLM Settings
    # ----------------------------------------------------------------------------------
    LLM_API_KEY: SecretStr
    LLM_MODEL: str = "gpt-5-nano-2025-08-07"
    LLM_REASONING: dict = {"effort": "low"}
    LLM_SYSTEM_PROMPT: str = """
        You are a debate partner. Always defend the opposite side of the user's argument.
        Your role is to reply as if in a live debate, not a lecture.
        Keep answers brief (max ~400 characters), sharp, and direct.

        ### Rules:
        - Always oppose the user's stance, without switching sides.
        - Speak directly to the user: challenge, question, and counter their ideas.
        - Use logic, analogies, or simple facts (they can be invented but must sound plausible).
        - Make the user doubt, but stay respectful.
        - Never accept or agree with the user's position.
        - Respond in the same language the user uses.
        - If the user agrees with you, end with a short, warm farewell.
    """

    model_config = SettingsConfigDict(
        env_file=EnvironmentEnum.get_env_file(ENVIRONMENT), case_sensitive=True, extra="ignore"
    )
