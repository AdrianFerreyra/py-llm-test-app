import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.application.dtos import (
    LLMCompleted,
    LLMMessageChunk,
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMToolCallMessageDTO,
    LLMToolCallOutputMessageDTO,
    LLMToolCallResponseDTO,
)
from src.application.ports import LLMPort
from src.domain import WeatherInfo
from src.infra.adapters.openai_llm_adapter import OpenAILLMAdapter


class TestOpenAILLMAdapter:
    @pytest.mark.asyncio
    async def test_call_sends_messages_and_tools_to_openai(self):
        async def mock_stream():
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "message"
            done_event.item.content = [Mock(text="The weather in Paris is sunny and 15°C.")]
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What is the weather like in Paris today?"
                    )
                ]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            mock_client.responses.create.assert_called_once()
            call_kwargs = mock_client.responses.create.call_args.kwargs
            assert call_kwargs["model"] == "gpt-4.1"
            assert call_kwargs["input"] == [
                {"role": "user", "content": "What is the weather like in Paris today?"},
            ]
            assert call_kwargs["tools"] == OpenAILLMAdapter.available_tools
            assert call_kwargs["stream"] is True

    @pytest.mark.asyncio
    async def test_call_formats_tool_call_output_message_correctly(self):
        weather = WeatherInfo(
            temperature_c=20.0,
            temperature_f=68.0,
            feels_like_c=19.0,
            feels_like_f=66.0,
            humidity=50,
            pressure_mb=1013.0,
            pressure_in=29.9,
            condition="Sunny",
            condition_icon="sunny.png",
            wind_mph=5.0,
            wind_kph=8.0,
            wind_direction="N",
            wind_degree=0,
            visibility_km=10.0,
            visibility_miles=6.0,
            uv_index=5.0,
            cloud_cover=10,
            last_updated="2024-01-01 12:00",
        )

        async def mock_stream():
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "message"
            done_event.item.content = [Mock(text="The weather in London is sunny!")]
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What's the weather in London?"
                    ),
                    LLMToolCallOutputMessageDTO(
                        call_id="call_abc123",
                        output=weather,
                    ),
                ]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            call_args = mock_client.responses.create.call_args
            input_messages = call_args.kwargs["input"]

            assert len(input_messages) == 2
            assert input_messages[0] == {
                "role": "user",
                "content": "What's the weather in London?",
            }
            assert input_messages[1]["type"] == "function_call_output"
            assert input_messages[1]["call_id"] == "call_abc123"
            output_data = json.loads(input_messages[1]["output"])
            assert output_data["temperature_c"] == 20.0
            assert output_data["condition"] == "Sunny"

    @pytest.mark.asyncio
    async def test_call_formats_tool_call_message_as_function_call(self):
        """
        When the conversation includes a tool call from the assistant,
        it must be formatted as a function_call object, not a text message.
        OpenAI requires this format when followed by a function_call_output.
        """
        weather = WeatherInfo(
            temperature_c=20.0,
            temperature_f=68.0,
            feels_like_c=19.0,
            feels_like_f=66.0,
            humidity=50,
            pressure_mb=1013.0,
            pressure_in=29.9,
            condition="Sunny",
            condition_icon="sunny.png",
            wind_mph=5.0,
            wind_kph=8.0,
            wind_direction="N",
            wind_degree=0,
            visibility_km=10.0,
            visibility_miles=6.0,
            uv_index=5.0,
            cloud_cover=10,
            last_updated="2024-01-01 12:00",
        )

        async def mock_stream():
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "message"
            done_event.item.content = [Mock(text="The weather in London is sunny, 20°C!")]
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            # This is the conversation after a tool call:
            # 1. User asks about weather
            # 2. Assistant made a tool call (LLMToolCallMessageDTO)
            # 3. Tool returned result (LLMToolCallOutputMessageDTO)
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What's the weather in London?"
                    ),
                    LLMToolCallMessageDTO(
                        call_id="call_abc123",
                        function_name="get_current_weather",
                        arguments={"location": "London"},
                    ),
                    LLMToolCallOutputMessageDTO(
                        call_id="call_abc123",
                        output=weather,
                    ),
                ]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            call_args = mock_client.responses.create.call_args
            input_messages = call_args.kwargs["input"]

            assert len(input_messages) == 3

            # First message: user request
            assert input_messages[0] == {
                "role": "user",
                "content": "What's the weather in London?",
            }

            # Second message: assistant's tool call (must be function_call format)
            assert input_messages[1]["type"] == "function_call"
            assert input_messages[1]["call_id"] == "call_abc123"
            assert input_messages[1]["name"] == "get_current_weather"
            assert json.loads(input_messages[1]["arguments"]) == {"location": "London"}

            # Third message: tool output
            assert input_messages[2]["type"] == "function_call_output"
            assert input_messages[2]["call_id"] == "call_abc123"

    def test_implements_llm_port(self):
        with patch("src.infra.adapters.openai_llm_adapter.AsyncOpenAI"):
            adapter = OpenAILLMAdapter(api_key="test-api-key")
            assert isinstance(adapter, LLMPort)


class TestOpenAILLMAdapterStreaming:
    @pytest.mark.asyncio
    async def test_call_yields_message_chunks_from_stream(self):
        """When OpenAI streams text deltas, adapter yields LLMMessageChunk events."""

        async def mock_stream():
            # Simulate streaming response with text deltas
            delta1 = Mock()
            delta1.type = "response.output_text.delta"
            delta1.delta = "Hello"
            yield delta1

            delta2 = Mock()
            delta2.type = "response.output_text.delta"
            delta2.delta = ", world!"
            yield delta2

            # Final event when message is done
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "message"
            done_event.item.content = [Mock(text="Hello, world!")]
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[LLMRequestMessageDTO(role="user", content="Hi")]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            assert len(events) == 3
            assert isinstance(events[0], LLMMessageChunk)
            assert events[0].content == "Hello"
            assert isinstance(events[1], LLMMessageChunk)
            assert events[1].content == ", world!"
            assert isinstance(events[2], LLMCompleted)
            assert isinstance(events[2].final_response, LLMMessageResponseDTO)
            assert events[2].final_response.message == "Hello, world!"

    @pytest.mark.asyncio
    async def test_call_yields_completed_with_tool_call_response(self):
        """When OpenAI returns a tool call, adapter yields LLMCompleted with LLMToolCallResponseDTO."""

        async def mock_stream():
            # Tool call done event
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "function_call"
            done_event.item.call_id = "call_abc123"
            done_event.item.name = "get_current_weather"
            done_event.item.arguments = '{"location": "London"}'
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What's the weather in London?"
                    )
                ]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            assert len(events) == 1
            assert isinstance(events[0], LLMCompleted)
            assert isinstance(events[0].final_response, LLMToolCallResponseDTO)
            assert events[0].final_response.call_id == "call_abc123"
            assert events[0].final_response.function_name == "get_current_weather"
            assert events[0].final_response.arguments == {"location": "London"}

    @pytest.mark.asyncio
    async def test_call_uses_streaming_api(self):
        """Verifies that the adapter uses the streaming API with stream=True."""

        async def mock_stream():
            done_event = Mock()
            done_event.type = "response.output_item.done"
            done_event.item = Mock()
            done_event.item.type = "message"
            done_event.item.content = [Mock(text="Hi!")]
            yield done_event

        with patch(
            "src.infra.adapters.openai_llm_adapter.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_stream()

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[LLMRequestMessageDTO(role="user", content="Hi")]
            )

            events = []
            async for event in adapter.call(request):
                events.append(event)

            mock_client.responses.create.assert_called_once()
            call_kwargs = mock_client.responses.create.call_args.kwargs
            assert call_kwargs.get("stream") is True
