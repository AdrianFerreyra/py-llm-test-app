from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMResponseDTO,
    LLMToolCallResponseDTO,
)
from src.application.ports import LLMPort


class FakeLLMAdapter(LLMPort):
    def __init__(self, response: LLMResponseDTO):
        self.response = response
        self.calls: list[LLMRequestDTO] = []

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        self.calls.append(request)
        return self.response


class TestLLMPort:
    def test_call_returns_message_response_dto(self):
        response = LLMMessageResponseDTO(message="Hello, how can I help?")
        adapter = FakeLLMAdapter(response=response)
        request = LLMRequestDTO(
            messages=[LLMRequestMessageDTO(role="user", content="Hi there")]
        )

        result = adapter.call(request)

        assert isinstance(result, LLMMessageResponseDTO)
        assert result.message == "Hello, how can I help?"
        assert adapter.calls == [request]

    def test_call_returns_tool_call_response_dto(self):
        response = LLMToolCallResponseDTO(
            call_id="call_abc123",
            function_name="get_weather",
            arguments={"location": "London"},
        )
        adapter = FakeLLMAdapter(response=response)
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
        assert result.function_name == "get_weather"
        assert result.arguments == {"location": "London"}
        assert adapter.calls == [request]
