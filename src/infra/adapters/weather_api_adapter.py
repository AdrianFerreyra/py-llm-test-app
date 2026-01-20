import requests

from src.application.ports import WeatherPort


class WeatherApiAdapter(WeatherPort):
    BASE_URL = "https://weather-test-907656039105.europe-west2.run.app"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, location: str) -> str:
        response = requests.get(
            self.BASE_URL,
            headers={"X-API-Key": self.api_key},
            params={"location": location},
        )
        response.raise_for_status()
        return response.text
