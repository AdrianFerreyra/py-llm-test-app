from src.application.dtos import LLMRequestDTO, LLMToolCallMessageDTO, LLMToolCallOutputMessageDTO
from src.application.translators import conversation_to_llm_request
from src.domain import (
    Conversation,
    LLMMessage,
    LLMToolCallMessage,
    ToolCallOutputMessage,
    UserMessage,
    WeatherInfo,
)


class TestConversationToLLMRequest:
    def test_transforms_empty_conversation(self):
        conversation = Conversation(messages=[])

        result = conversation_to_llm_request(conversation)

        assert isinstance(result, LLMRequestDTO)
        assert result.messages == []

    def test_transforms_user_message_to_user_role(self):
        conversation = Conversation(messages=[
            UserMessage(content="Hello!"),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 1
        assert result.messages[0].role == "user"
        assert result.messages[0].content == "Hello!"

    def test_transforms_llm_message_to_assistant_role(self):
        conversation = Conversation(messages=[
            LLMMessage(content="Hi there!"),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 1
        assert result.messages[0].role == "assistant"
        assert result.messages[0].content == "Hi there!"

    def test_transforms_full_conversation(self):
        conversation = Conversation(messages=[
            UserMessage(content="Hello"),
            LLMMessage(content="Hi! How can I help?"),
            UserMessage(content="What's the weather?"),
            LLMMessage(content="I can check that for you."),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 4
        assert result.messages[0].role == "user"
        assert result.messages[0].content == "Hello"
        assert result.messages[1].role == "assistant"
        assert result.messages[1].content == "Hi! How can I help?"
        assert result.messages[2].role == "user"
        assert result.messages[2].content == "What's the weather?"
        assert result.messages[3].role == "assistant"
        assert result.messages[3].content == "I can check that for you."

    def test_transforms_tool_call_message_to_tool_call_dto(self):
        conversation = Conversation(messages=[
            LLMToolCallMessage(
                call_id="call_abc123",
                function_name="get_weather",
                arguments={"location": "London"},
            ),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 1
        assert isinstance(result.messages[0], LLMToolCallMessageDTO)
        assert result.messages[0].call_id == "call_abc123"
        assert result.messages[0].function_name == "get_weather"
        assert result.messages[0].arguments == {"location": "London"}

    def test_transforms_tool_call_output_message_to_tool_call_output_dto(self):
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
        conversation = Conversation(messages=[
            ToolCallOutputMessage(call_id="call_abc123", output=weather),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 1
        assert isinstance(result.messages[0], LLMToolCallOutputMessageDTO)
        assert result.messages[0].call_id == "call_abc123"
        assert result.messages[0].output == weather
