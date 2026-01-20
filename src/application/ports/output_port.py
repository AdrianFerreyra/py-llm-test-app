from abc import ABC, abstractmethod


class OutputPort(ABC):
    @abstractmethod
    def write(self, message: str) -> None:
        pass
