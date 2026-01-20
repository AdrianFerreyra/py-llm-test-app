from abc import ABC, abstractmethod

from src.application.dtos import LLMResponseDTO


class LLMPort(ABC):
    @abstractmethod
    def call(self, message: str) -> LLMResponseDTO:
        pass
