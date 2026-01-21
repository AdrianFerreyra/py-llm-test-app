# py-llm-test-app

A CLI chatbot application that uses OpenAI's GPT-4.1 API with streaming responses and tool calling support. Built with clean architecture principles (hexagonal/ports-and-adapters pattern).

## Features

- Interactive CLI chat interface
- Streaming responses (text appears as it's generated)
- Tool calling support (currently supports weather queries)
- Conversation history maintained across turns
- Clean architecture with dependency injection

## Architecture

The project follows hexagonal architecture:

```
src/
├── application/          # Application layer
│   ├── ports/            # Abstract interfaces (InputPort, OutputPort, LLMPort, WeatherPort)
│   ├── dtos/             # Data transfer objects
│   ├── translators/      # DTO converters
│   └── application_service.py
├── domain/               # Domain models
│   └── models/           # Conversation, Message types
└── infra/                # Infrastructure adapters
    └── adapters/         # OpenAI, stdin/stdout, Weather API implementations
```

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Weather API key (from [WeatherAPI.com](https://www.weatherapi.com/))

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd py-llm-test-app
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   WEATHER_API_KEY=your_weather_api_key_here
   ```

## Running the Application

```bash
uv run python main.py
```

Once running, type your messages and press Enter. The assistant will respond with streaming text. You can ask about the weather in any city, and the app will use tool calling to fetch real weather data.

To exit, type `quit`, `exit`, or `q`.

### Example

```
> What's the weather like in London?
The weather in London is currently partly cloudy with a temperature of 12°C...

> Tell me a joke
Why don't scientists trust atoms? Because they make up everything!

> quit
```

## Running Tests

Run all tests:
```bash
uv run pytest tests/ -v
```

Run a specific test file:
```bash
uv run pytest tests/unit/test_application_service_run.py -v
```

Run tests with coverage (if coverage is installed):
```bash
uv run pytest tests/ --cov=src
```
