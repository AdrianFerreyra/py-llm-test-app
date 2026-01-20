from unittest.mock import Mock, patch

from src.application.dtos import WeatherDTO
from src.infra.adapters.weather_api_adapter import WeatherApiAdapter


class TestWeatherApiAdapter:
    def test_get_weather_calls_api_and_returns_weather_dto(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "current": {
                "temperature_c": 27.4,
                "temperature_f": 81.3,
                "feels_like_c": 26.0,
                "feels_like_f": 78.8,
                "humidity": 32,
                "pressure_mb": 1015.0,
                "pressure_in": 29.97,
                "condition": "Sunny",
                "condition_icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                "wind_mph": 11.2,
                "wind_kph": 18.0,
                "wind_direction": "ENE",
                "wind_degree": 69,
                "visibility_km": 10.0,
                "visibility_miles": 6.0,
                "uv_index": 1.3,
                "cloud_cover": 0,
                "last_updated": "2026-01-20 18:45",
            }
        }
        mock_response.raise_for_status = Mock()

        with patch("src.infra.adapters.weather_api_adapter.requests.get") as mock_get:
            mock_get.return_value = mock_response

            adapter = WeatherApiAdapter(api_key="test-api-key")
            result = adapter.get_weather("Zakynthos")

            mock_get.assert_called_once_with(
                "https://weather-test-907656039105.europe-west2.run.app",
                headers={"X-API-Key": "test-api-key"},
                params={"location": "Zakynthos"},
            )
            assert isinstance(result, WeatherDTO)
            assert result.temperature_c == 27.4
            assert result.condition == "Sunny"
            assert result.humidity == 32
