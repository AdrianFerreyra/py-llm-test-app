from unittest.mock import Mock, patch

from src.infra.adapters.weather_api_adapter import WeatherApiAdapter


class TestWeatherApiAdapter:
    def test_get_weather_calls_api_with_correct_params(self):
        mock_response = Mock()
        mock_response.text = "Sunny, 28°C"
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
            assert result == "Sunny, 28°C"
