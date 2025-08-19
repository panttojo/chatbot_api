import os

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

    # Project Settings
    # ----------------------------------------------------------------------------------
    DESCRIPTION: str = "Chatbot API"
    VERSION: str = "0.1.0"

    CORS_ALLOWED_ORIGINS: list[str] = []

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str

    model_config = SettingsConfigDict(
        env_file=EnvironmentEnum.get_env_file(ENVIRONMENT), case_sensitive=True, extra="ignore"
    )
