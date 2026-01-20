from abc import ABC, abstractmethod


class InputPort(ABC):
    @abstractmethod
    def read(self) -> str:
        pass
