from abc import ABC, abstractmethod


class LLMPort(ABC):
    @abstractmethod
    def call(self, message: str) -> str:
        pass
