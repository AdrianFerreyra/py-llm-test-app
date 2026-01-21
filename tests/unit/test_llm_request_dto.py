from src.application.dtos import (
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMToolCallOutputMessageDTO,
)
from src.domain import WeatherInfo


class TestLLMRequestMessageDTO:
    def test_stores_role_and_content(self):
        message = LLMRequestMessageDTO(role="user", content="Hello!")

        assert message.role == "user"
        assert message.content == "Hello!"


class TestLLMToolCallOutputMessageDTO:
    def test_stores_call_id_and_output(self):
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
        message = LLMToolCallOutputMessageDTO(call_id="call_abc123", output=weather)

        assert message.call_id == "call_abc123"
        assert message.output == weather

    def test_inherits_from_llm_request_message_dto(self):
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
        message = LLMToolCallOutputMessageDTO(call_id="call_abc123", output=weather)

        assert isinstance(message, LLMRequestMessageDTO)


class TestLLMRequestDTO:
    def test_stores_list_of_messages(self):
        messages = [
            LLMRequestMessageDTO(role="user", content="Hello"),
            LLMRequestMessageDTO(role="assistant", content="Hi there!"),
        ]
        request = LLMRequestDTO(messages=messages)

        assert len(request.messages) == 2
        assert request.messages[0].role == "user"
        assert request.messages[0].content == "Hello"
        assert request.messages[1].role == "assistant"
        assert request.messages[1].content == "Hi there!"

    def test_empty_messages(self):
        request = LLMRequestDTO(messages=[])

        assert request.messages == []
