from src.application import ApplicationService
from src.application.dtos import WeatherDTO
from src.application.ports import InputPort, OutputPort, WeatherPort
from src.domain import WeatherInfo


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class FakeOutputAdapter(OutputPort):
    def __init__(self):
        self.messages: list = []

    def write(self, message) -> None:
        self.messages.append(message)


class FakeWeatherAdapter(WeatherPort):
    def __init__(self, responses: dict[str, WeatherDTO]):
        self.responses = responses
        self.calls: list[str] = []

    def get_weather(self, location: str) -> WeatherDTO:
        self.calls.append(location)
        return self.responses[location]


def make_weather_dto(condition: str, temp_c: float = 20.0) -> WeatherDTO:
    return WeatherDTO(
        temperature_c=temp_c,
        temperature_f=68.0,
        feels_like_c=19.0,
        feels_like_f=66.0,
        humidity=50,
        pressure_mb=1015.0,
        pressure_in=29.97,
        condition=condition,
        condition_icon="//icon.png",
        wind_mph=10.0,
        wind_kph=16.0,
        wind_direction="N",
        wind_degree=0,
        visibility_km=10.0,
        visibility_miles=6.0,
        uv_index=1.0,
        cloud_cover=0,
        last_updated="2026-01-20 18:00",
    )


class TestApplicationServiceRun:
    def test_run_calls_weather_port_and_outputs_weather_info(self):
        fake_input = FakeInputAdapter(["London", "Paris", "exit"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({
            "London": make_weather_dto("Sunny", 10.0),
            "Paris": make_weather_dto("Cloudy", 12.0),
        })
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["London", "Paris"]
        assert len(fake_output.messages) == 2
        assert isinstance(fake_output.messages[0], WeatherInfo)
        assert fake_output.messages[0].condition == "Sunny"
        assert fake_output.messages[0].temperature_c == 10.0
        assert isinstance(fake_output.messages[1], WeatherInfo)
        assert fake_output.messages[1].condition == "Cloudy"

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["London", "quit"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({"London": make_weather_dto("Sunny")})
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["London"]
        assert len(fake_output.messages) == 1

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["Berlin", "q"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({"Berlin": make_weather_dto("Rainy")})
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["Berlin"]
        assert len(fake_output.messages) == 1
