from src.application.ports import WeatherPort


class ApplicationService:
    def __init__(self, weather_port: WeatherPort | None = None):
        self.weather_port = weather_port

    def run(self) -> None:
        while True:
            user_input = input("> ")
            if not user_input:
                break
            message = user_input.rstrip()
            if message in ("quit", "exit", "q"):
                break
            print(message)

    # used for testing only. TODO remove.
    def get_weather(self, location: str) -> str:
        return self.weather_port.get_weather(location)
