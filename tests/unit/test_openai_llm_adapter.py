from unittest.mock import Mock, patch

from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
)
from src.application.ports import LLMPort
from src.infra.adapters.openai_llm_adapter import OpenAILLMAdapter


class TestOpenAILLMAdapter:
    def test_call_sends_messages_to_openai_and_returns_message_response_dto(self):
        mock_response = Mock()
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

            mock_client.responses.create.assert_called_once_with(
                model="gpt-4.1",
                input=[
                    {"role": "user", "content": "What is the weather like in Paris today?"},
                ],
            )
            assert isinstance(result, LLMMessageResponseDTO)
            assert result.message == "The weather in Paris is sunny and 15°C."

    def test_call_converts_multiple_messages_to_openai_format(self):
        mock_response = Mock()
        mock_response.output_text = "I can help with that."

        with patch("src.infra.adapters.openai_llm_adapter.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            mock_client.responses.create.return_value = mock_response

            adapter = OpenAILLMAdapter(api_key="test-api-key")
            request = LLMRequestDTO(
                messages=[
                    LLMRequestMessageDTO(role="user", content="Hello"),
                    LLMRequestMessageDTO(role="assistant", content="Hi there!"),
                    LLMRequestMessageDTO(role="user", content="Help me please"),
                ]
            )
            result = adapter.call(request)

            mock_client.responses.create.assert_called_once_with(
                model="gpt-4.1",
                input=[
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"},
                    {"role": "user", "content": "Help me please"},
                ],
            )
            assert isinstance(result, LLMMessageResponseDTO)

    def test_implements_llm_port(self):
        with patch("src.infra.adapters.openai_llm_adapter.OpenAI"):
            adapter = OpenAILLMAdapter(api_key="test-api-key")
            assert isinstance(adapter, LLMPort)
