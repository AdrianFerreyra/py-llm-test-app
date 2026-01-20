from abc import ABC, abstractmethod

from src.application.dtos import WeatherDTO


class WeatherPort(ABC):
    @abstractmethod
    def get_weather(self, location: str) -> WeatherDTO:
        pass
