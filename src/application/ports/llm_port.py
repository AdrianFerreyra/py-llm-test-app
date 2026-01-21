from abc import ABC, abstractmethod

from src.application.dtos import LLMRequestDTO, LLMResponseDTO


class LLMPort(ABC):
    @abstractmethod
    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        pass
