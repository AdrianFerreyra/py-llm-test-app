import os

from dotenv import load_dotenv

from src.adapters import WeatherApiAdapter
from src.application import ApplicationService

load_dotenv()


def main():
    weather_adapter = WeatherApiAdapter(api_key=os.getenv("WEATHER_API_KEY"))
    app = ApplicationService(weather_port=weather_adapter)

    app.run()



if __name__ == "__main__":
    main()
