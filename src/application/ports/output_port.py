from abc import ABC, abstractmethod


class OutputPort(ABC):
    @abstractmethod
    async def write(self, message: str) -> None:
        pass
    
    @abstractmethod
    def flush(self) -> None:
        pass