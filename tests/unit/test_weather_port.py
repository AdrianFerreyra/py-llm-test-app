from src.application import ApplicationService
from src.application.ports import WeatherPort


class FakeWeatherAdapter(WeatherPort):
    def __init__(self, fake_response: str):
        self.fake_response = fake_response

    def get_weather(self, location: str) -> str:
        return self.fake_response


class TestWeatherPort:
    def test_get_weather_returns_data_from_adapter(self):
        fake_weather = FakeWeatherAdapter(fake_response="Sunny, 25°C")
        app = ApplicationService(weather_port=fake_weather)

        result = app.get_weather("London")

        assert result == "Sunny, 25°C"
