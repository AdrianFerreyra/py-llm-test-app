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
            message = user_input.rstrip()
            if message in ("quit", "exit", "q"):
                break
            self.output_port.write(message)

    def get_weather(self, location: str) -> str:
        return self.weather_port.get_weather(location)
