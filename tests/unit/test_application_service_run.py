from src.application import ApplicationService
from src.application.ports import InputPort, OutputPort, WeatherPort


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class FakeOutputAdapter(OutputPort):
    def __init__(self):
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)


class FakeWeatherAdapter(WeatherPort):
    def __init__(self, responses: dict[str, str]):
        self.responses = responses
        self.calls: list[str] = []

    def get_weather(self, location: str) -> str:
        self.calls.append(location)
        return self.responses.get(location, '{"error": "not found"}')


class TestApplicationServiceRun:
    def test_run_calls_weather_port_with_user_input_and_outputs_response(self):
        fake_input = FakeInputAdapter(["London", "Paris", "exit"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({
            "London": '{"location": "London", "temp": "10°C"}',
            "Paris": '{"location": "Paris", "temp": "12°C"}',
        })
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["London", "Paris"]
        assert '{"location": "London", "temp": "10°C"}' in fake_output.messages
        assert '{"location": "Paris", "temp": "12°C"}' in fake_output.messages

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["London", "quit"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({"London": '{"temp": "10°C"}'})
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["London"]
        assert "quit" not in fake_output.messages

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["Berlin", "q"])
        fake_output = FakeOutputAdapter()
        fake_weather = FakeWeatherAdapter({"Berlin": '{"temp": "8°C"}'})
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["Berlin"]
        assert "q" not in fake_output.messages
