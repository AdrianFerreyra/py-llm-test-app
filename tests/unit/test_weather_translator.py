from src.application.dtos import WeatherDTO
from src.application.translators import weather_dto_to_info
from src.domain import WeatherInfo


class TestWeatherTranslator:
    def test_translates_weather_dto_to_weather_info(self):
        dto = WeatherDTO(
            temperature_c=27.4,
            temperature_f=81.3,
            feels_like_c=26.0,
            feels_like_f=78.8,
            humidity=32,
            pressure_mb=1015.0,
            pressure_in=29.97,
            condition="Sunny",
            condition_icon="//cdn.weatherapi.com/weather/64x64/day/113.png",
            wind_mph=11.2,
            wind_kph=18.0,
            wind_direction="ENE",
            wind_degree=69,
            visibility_km=10.0,
            visibility_miles=6.0,
            uv_index=1.3,
            cloud_cover=0,
            last_updated="2026-01-20 18:45",
        )

        result = weather_dto_to_info(dto)

        assert isinstance(result, WeatherInfo)
        assert result.temperature_c == 27.4
        assert result.temperature_f == 81.3
        assert result.feels_like_c == 26.0
        assert result.feels_like_f == 78.8
        assert result.humidity == 32
        assert result.pressure_mb == 1015.0
        assert result.pressure_in == 29.97
        assert result.condition == "Sunny"
        assert result.condition_icon == "//cdn.weatherapi.com/weather/64x64/day/113.png"
        assert result.wind_mph == 11.2
        assert result.wind_kph == 18.0
        assert result.wind_direction == "ENE"
        assert result.wind_degree == 69
        assert result.visibility_km == 10.0
        assert result.visibility_miles == 6.0
        assert result.uv_index == 1.3
        assert result.cloud_cover == 0
        assert result.last_updated == "2026-01-20 18:45"
