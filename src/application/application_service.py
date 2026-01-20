from src.application.ports import InputPort, OutputPort, WeatherPort


class ApplicationService:
    def __init__(
        self,
        input_port: InputPort | None = None,
        output_port: OutputPort | None = None,
        weather_port: WeatherPort | None = None,
    ):
        self.input_port = input_port
        self.output_port = output_port
        self.weather_port = weather_port

    def run(self) -> None:
        while True:
            user_input = self.input_port.read()
            if not user_input:
                break
            location = user_input.rstrip()
            if location in ("quit", "exit", "q"):
                break
            weather_data = self.weather_port.get_weather(location)
            self.output_port.write(weather_data)
