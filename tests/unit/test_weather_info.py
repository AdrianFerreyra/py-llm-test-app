from src.domain import WeatherInfo


class TestWeatherInfo:
    def test_stores_all_weather_fields(self):
        weather = WeatherInfo(
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

        assert weather.temperature_c == 27.4
        assert weather.temperature_f == 81.3
        assert weather.feels_like_c == 26.0
        assert weather.feels_like_f == 78.8
        assert weather.humidity == 32
        assert weather.pressure_mb == 1015.0
        assert weather.pressure_in == 29.97
        assert weather.condition == "Sunny"
        assert weather.condition_icon == "//cdn.weatherapi.com/weather/64x64/day/113.png"
        assert weather.wind_mph == 11.2
        assert weather.wind_kph == 18.0
        assert weather.wind_direction == "ENE"
        assert weather.wind_degree == 69
        assert weather.visibility_km == 10.0
        assert weather.visibility_miles == 6.0
        assert weather.uv_index == 1.3
        assert weather.cloud_cover == 0
        assert weather.last_updated == "2026-01-20 18:45"
