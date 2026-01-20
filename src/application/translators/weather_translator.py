from src.application.dtos import WeatherDTO
from src.domain import WeatherInfo


def weather_dto_to_info(dto: WeatherDTO) -> WeatherInfo:
    return WeatherInfo(
        temperature_c=dto.temperature_c,
        temperature_f=dto.temperature_f,
        feels_like_c=dto.feels_like_c,
        feels_like_f=dto.feels_like_f,
        humidity=dto.humidity,
        pressure_mb=dto.pressure_mb,
        pressure_in=dto.pressure_in,
        condition=dto.condition,
        condition_icon=dto.condition_icon,
        wind_mph=dto.wind_mph,
        wind_kph=dto.wind_kph,
        wind_direction=dto.wind_direction,
        wind_degree=dto.wind_degree,
        visibility_km=dto.visibility_km,
        visibility_miles=dto.visibility_miles,
        uv_index=dto.uv_index,
        cloud_cover=dto.cloud_cover,
        last_updated=dto.last_updated,
    )
