from src.application.ports import InputPort, LLMPort, OutputPort, WeatherPort


class ApplicationService:
    def __init__(
        self,
        input_port: InputPort | None = None,
        output_port: OutputPort | None = None,
        llm_port: LLMPort | None = None,
        weather_port: WeatherPort | None = None,
    ):
        self.input_port = input_port
        self.output_port = output_port
        self.llm_port = llm_port
        self.weather_port = weather_port

    def run(self) -> None:
        while True:
            user_input = self.input_port.read()
            if not user_input:
                break
            message = user_input.rstrip()
            if message in ("quit", "exit", "q"):
                break
            response = self.llm_port.call(message)
            self.output_port.write(response)
