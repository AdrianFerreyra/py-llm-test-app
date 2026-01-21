from src.domain import (
    LLMMessage,
    LLMToolCallMessage,
    Message,
    ToolCallOutputMessage,
    UserMessage,
    WeatherInfo,
)


class TestMessage:
    def test_user_message_inherits_from_message(self):
        msg = UserMessage(content="Hello!")

        assert isinstance(msg, Message)

    def test_llm_message_inherits_from_message(self):
        msg = LLMMessage(content="Hi there!")

        assert isinstance(msg, Message)

    def test_llm_tool_call_message_inherits_from_message(self):
        msg = LLMToolCallMessage(
            call_id="call_123",
            function_name="get_weather",
            arguments={"location": "London"},
        )

        assert isinstance(msg, Message)

    def test_tool_call_output_message_inherits_from_message(self):
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
        msg = ToolCallOutputMessage(call_id="call_123", output=weather)

        assert isinstance(msg, Message)


class TestUserMessage:
    def test_stores_content(self):
        msg = UserMessage(content="What's the weather?")

        assert msg.content == "What's the weather?"


class TestLLMMessage:
    def test_stores_content(self):
        msg = LLMMessage(content="The weather is sunny.")

        assert msg.content == "The weather is sunny."


class TestLLMToolCallMessage:
    def test_stores_call_id_function_name_and_arguments(self):
        msg = LLMToolCallMessage(
            call_id="call_abc123",
            function_name="get_weather",
            arguments={"location": "Paris", "unit": "celsius"},
        )

        assert msg.call_id == "call_abc123"
        assert msg.function_name == "get_weather"
        assert msg.arguments == {"location": "Paris", "unit": "celsius"}

    def test_arguments_can_be_empty(self):
        msg = LLMToolCallMessage(
            call_id="call_empty_args",
            function_name="get_current_time",
            arguments={},
        )

        assert msg.call_id == "call_empty_args"
        assert msg.function_name == "get_current_time"
        assert msg.arguments == {}


class TestToolCallOutputMessage:
    def test_stores_call_id_and_output(self):
        weather = WeatherInfo(
            temperature_c=25.0,
            temperature_f=77.0,
            feels_like_c=24.0,
            feels_like_f=75.0,
            humidity=40,
            pressure_mb=1015.0,
            pressure_in=30.0,
            condition="Sunny",
            condition_icon="sunny.png",
            wind_mph=3.0,
            wind_kph=5.0,
            wind_direction="W",
            wind_degree=270,
            visibility_km=15.0,
            visibility_miles=9.0,
            uv_index=7.0,
            cloud_cover=5,
            last_updated="2024-01-01 14:00",
        )
        msg = ToolCallOutputMessage(call_id="call_abc123", output=weather)

        assert msg.call_id == "call_abc123"
        assert msg.output == weather
