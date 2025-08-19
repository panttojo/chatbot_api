from typing import ClassVar

from core.settings.base import Settings


class LocalSettings(Settings):
    # Log Settings
    # ----------------------------------------------------------------------------------
    DEBUG: bool = True
    COLORIZE_LOG: bool = True
    SERIALIZE_LOG: bool = False

    # Project Settings
    # ----------------------------------------------------------------------------------
    CORS_ALLOWED_ORIGINS: ClassVar[list[str]] = ["http://localhost:8000"]

    # Third Party Settings
    # ----------------------------------------------------------------------------------
    SENTRY_DSN: str | None = None
