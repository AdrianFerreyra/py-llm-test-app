import json
from unittest.mock import Mock, patch

from src.application.dtos import (
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
    def test_call_sends_messages_and_tools_to_openai(self):
        mock_response = Mock()
        mock_response.output = []
        mock_response.output_text = "The weather in Paris is sunny and 15°C."

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What is the weather like in Paris today?"
                    )
                ]
            )
            adapter.call(request)

            mock_client.responses.create.assert_called_once_with(
                model="gpt-4.1",
                input=[
                    {"role": "user", "content": "What is the weather like in Paris today?"},
                ],
                tools=OpenAILLMAdapter.available_tools,
            )

    def test_call_formats_tool_call_output_message_correctly(self):
        mock_response = Mock()
        mock_response.output = []
        mock_response.output_text = "The weather in London is sunny!"

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

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

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
            adapter.call(request)

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

    def test_call_returns_message_response_dto_for_text_response(self):
        mock_response = Mock()
        mock_response.output = []
        mock_response.output_text = "The weather in Paris is sunny and 15°C."

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What is the weather like in Paris today?"
                    )
                ]
            )
            result = adapter.call(request)

            assert isinstance(result, LLMMessageResponseDTO)
            assert result.message == "The weather in Paris is sunny and 15°C."

    def test_call_returns_tool_call_response_dto_when_openai_requests_tool(self):
        mock_function_call = Mock()
        mock_function_call.type = "function_call"
        mock_function_call.call_id = "call_abc123"
        mock_function_call.name = "get_current_weather"
        mock_function_call.arguments = '{"location": "London"}'

        mock_response = Mock()
        mock_response.output = [mock_function_call]

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(
                        role="user", content="What's the weather in London?"
                    )
                ]
            )
            result = adapter.call(request)

            assert isinstance(result, LLMToolCallResponseDTO)
            assert result.call_id == "call_abc123"
            assert result.function_name == "get_current_weather"
            assert result.arguments == {"location": "London"}

    def test_call_formats_tool_call_message_as_function_call(self):
        """
        When the conversation includes a tool call from the assistant,
        it must be formatted as a function_call object, not a text message.
        OpenAI requires this format when followed by a function_call_output.
        """
        mock_response = Mock()
        mock_response.output = []
        mock_response.output_text = "The weather in London is sunny, 20°C!"

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

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

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
            adapter.call(request)

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
        with patch("src.infra.adapters.openai_llm_adapter.OpenAI"):
            adapter = OpenAILLMAdapter(api_key="test-api-key")
            assert isinstance(adapter, LLMPort)
