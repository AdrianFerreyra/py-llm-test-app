import asyncio
import os

from dotenv import load_dotenv

from src.application import ApplicationService
from src.infra import (
    OpenAILLMAdapter,
    StdInInputAdapter,
    StdOutOutputAdapter,
    WeatherApiAdapter,
)

load_dotenv()


async def main():
    input_adapter = StdInInputAdapter()
    output_adapter = StdOutOutputAdapter()
    llm_adapter = OpenAILLMAdapter(api_key=os.getenv("OPENAI_API_KEY"))
    weather_adapter = WeatherApiAdapter(api_key=os.getenv("WEATHER_API_KEY"))
    app = ApplicationService(
        input_port=input_adapter,
        output_port=output_adapter,
        llm_port=llm_adapter,
        weather_port=weather_adapter,
    )

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
