from abc import ABC, abstractmethod


class WeatherPort(ABC):
    @abstractmethod
    def get_weather(self, location: str) -> str:
        pass
