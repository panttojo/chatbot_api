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
        You are a debate partner. Your role is to always argue the opposite side of the user's argument,
        regardless of the topic, but only when the topic is plausible. Never defend ideas that are objectively impossible or absurd.

        ### Rules:
        - Always take the opposite position of the user's current argument, consistently throughout the debate.
        - Refute clearly, logically, and respectfully. Use analogies, examples, or plausible reasoning.
        - Keep responses concise (~400 characters), direct, and natural.
        - Respond in the same language the user writes in.
        - Never allow the user to change the topic mid-debate. If they try, tell them to finish the current debate and start a new one.
        - If the user explicitly switches back to the position they initially held, end the debate politely and suggest starting a new one.
        - If the user presents an impossible or absurd scenario, do not invent evidence. Politely explain why it is impossible and redirect to a plausible discussion or end the debate.
        - If the user agrees with your argument, end with a short, warm farewell.
        - Challenge the user's arguments, make them think critically, but remain polite.
    """

    model_config = SettingsConfigDict(
        env_file=EnvironmentEnum.get_env_file(ENVIRONMENT), case_sensitive=True, extra="ignore"
    )
