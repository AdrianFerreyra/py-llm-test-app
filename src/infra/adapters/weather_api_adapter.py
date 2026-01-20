import requests

from src.application.dtos import WeatherDTO
from src.application.ports import WeatherPort


class WeatherApiAdapter(WeatherPort):
    BASE_URL = "https://weather-test-907656039105.europe-west2.run.app"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, location: str) -> WeatherDTO:
        response = requests.get(
            self.BASE_URL,
            headers={"X-API-Key": self.api_key},
            params={"location": location},
        )
        response.raise_for_status()
        data = response.json()["current"]
        return WeatherDTO(
            temperature_c=data["temperature_c"],
            temperature_f=data["temperature_f"],
            feels_like_c=data["feels_like_c"],
            feels_like_f=data["feels_like_f"],
            humidity=data["humidity"],
            pressure_mb=data["pressure_mb"],
            pressure_in=data["pressure_in"],
            condition=data["condition"],
            condition_icon=data["condition_icon"],
            wind_mph=data["wind_mph"],
            wind_kph=data["wind_kph"],
            wind_direction=data["wind_direction"],
            wind_degree=data["wind_degree"],
            visibility_km=data["visibility_km"],
            visibility_miles=data["visibility_miles"],
            uv_index=data["uv_index"],
            cloud_cover=data["cloud_cover"],
            last_updated=data["last_updated"],
        )
