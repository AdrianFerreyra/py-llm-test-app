from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMResponseDTO,
    LLMToolCallResponseDTO,
)


class TestLLMResponseDTO:
    def test_llm_message_response_dto_inherits_from_llm_response_dto(self):
        response = LLMMessageResponseDTO(message="Hello!")

        assert isinstance(response, LLMResponseDTO)

    def test_llm_tool_call_response_dto_inherits_from_llm_response_dto(self):
        response = LLMToolCallResponseDTO(
            function_name="get_weather",
            arguments={"location": "London"},
        )

        assert isinstance(response, LLMResponseDTO)


class TestLLMMessageResponseDTO:
    def test_stores_message(self):
        response = LLMMessageResponseDTO(message="Hello, how can I help?")

        assert response.message == "Hello, how can I help?"


class TestLLMToolCallResponseDTO:
    def test_stores_function_name_and_arguments(self):
        response = LLMToolCallResponseDTO(
            function_name="get_weather",
            arguments={"location": "Paris", "unit": "celsius"},
        )

        assert response.function_name == "get_weather"
        assert response.arguments == {"location": "Paris", "unit": "celsius"}

    def test_arguments_can_be_empty(self):
        response = LLMToolCallResponseDTO(
            function_name="get_current_time",
            arguments={},
        )

        assert response.function_name == "get_current_time"
        assert response.arguments == {}
