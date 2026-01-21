from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from src.application.dtos import LLMRequestDTO, LLMStreamEvent


class LLMPort(ABC):
    @abstractmethod
    def call(self, request: LLMRequestDTO) -> AsyncIterator[LLMStreamEvent]:
        pass
