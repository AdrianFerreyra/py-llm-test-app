from dataclasses import dataclass


@dataclass
class WeatherDTO:
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: int
    pressure_mb: float
    pressure_in: float
    condition: str
    condition_icon: str
    wind_mph: float
    wind_kph: float
    wind_direction: str
    wind_degree: int
    visibility_km: float
    visibility_miles: float
    uv_index: float
    cloud_cover: int
    last_updated: str
