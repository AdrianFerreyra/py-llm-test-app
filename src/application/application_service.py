from src.application.ports import WeatherPort


class ApplicationService:
    def __init__(self, weather_port: WeatherPort | None = None):
        self.weather_port = weather_port

    def run(self) -> str:
        return "hello world"

    def get_weather(self, location: str) -> str:
        return self.weather_port.get_weather(location)
