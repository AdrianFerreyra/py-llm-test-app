from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMResponseDTO,
    LLMToolCallResponseDTO,
)
from src.application.ports import LLMPort


class FakeLLMAdapter(LLMPort):
    def __init__(self, response: LLMResponseDTO):
        self.response = response
        self.calls: list[str] = []

    def call(self, message: str) -> LLMResponseDTO:
        self.calls.append(message)
        return self.response


class TestLLMPort:
    def test_call_returns_message_response_dto(self):
        response = LLMMessageResponseDTO(message="Hello, how can I help?")
        adapter = FakeLLMAdapter(response=response)

        result = adapter.call("Hi there")

        assert isinstance(result, LLMMessageResponseDTO)
        assert result.message == "Hello, how can I help?"
        assert adapter.calls == ["Hi there"]

    def test_call_returns_tool_call_response_dto(self):
        response = LLMToolCallResponseDTO(
            function_name="get_weather",
            arguments={"location": "London"},
        )
        adapter = FakeLLMAdapter(response=response)

        result = adapter.call("What's the weather in London?")

        assert isinstance(result, LLMToolCallResponseDTO)
        assert result.function_name == "get_weather"
        assert result.arguments == {"location": "London"}
        assert adapter.calls == ["What's the weather in London?"]
