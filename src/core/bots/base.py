from abc import ABC, abstractmethod

from core.settings import settings


class BaseBot(ABC):
    prompt: str = settings.LLM_SYSTEM_PROMPT

    @abstractmethod
    def chat(self, message: str) -> str: ...
