import os

from dotenv import load_dotenv

from src.infra import StdInInputAdapter, StdOutOutputAdapter, WeatherApiAdapter
from src.application import ApplicationService

load_dotenv()


def main():
    input_adapter = StdInInputAdapter()
    output_adapter = StdOutOutputAdapter()
    weather_adapter = WeatherApiAdapter(api_key=os.getenv("WEATHER_API_KEY"))
    app = ApplicationService(
        input_port=input_adapter,
        output_port=output_adapter,
        weather_port=weather_adapter,
    )

    app.run()



if __name__ == "__main__":
    main()
