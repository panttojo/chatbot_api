from pydantic import SecretStr

from .base import Settings


class TestingsSettings(Settings):
    # Log Settings
    # ----------------------------------------------------------------------------------
    DEBUG: bool = True
    COLORIZE_LOG: bool = True
    SERIALIZE_LOG: bool = False

    # LLM Settings
    # ----------------------------------------------------------------------------------
    LLM_API_KEY: SecretStr = "test-123"

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str | None = None
