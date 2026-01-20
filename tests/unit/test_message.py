from src.domain import LLMMessage, LLMToolCallMessage, Message, UserMessage


class TestMessage:
    def test_user_message_inherits_from_message(self):
        msg = UserMessage(content="Hello!")

        assert isinstance(msg, Message)

    def test_llm_message_inherits_from_message(self):
        msg = LLMMessage(content="Hi there!")

        assert isinstance(msg, Message)

    def test_llm_tool_call_message_inherits_from_message(self):
        msg = LLMToolCallMessage(
            function_name="get_weather",
            arguments={"location": "London"},
        )

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
    def test_stores_function_name_and_arguments(self):
        msg = LLMToolCallMessage(
            function_name="get_weather",
            arguments={"location": "Paris", "unit": "celsius"},
        )

        assert msg.function_name == "get_weather"
        assert msg.arguments == {"location": "Paris", "unit": "celsius"}

    def test_arguments_can_be_empty(self):
        msg = LLMToolCallMessage(
            function_name="get_current_time",
            arguments={},
        )

        assert msg.function_name == "get_current_time"
        assert msg.arguments == {}
