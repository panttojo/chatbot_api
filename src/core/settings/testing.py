from .base import Settings


class TestingsSettings(Settings):
    # Log Settings
    # ----------------------------------------------------------------------------------
    DEBUG: bool = True
    COLORIZE_LOG: bool = True
    SERIALIZE_LOG: bool = False

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str | None = None
