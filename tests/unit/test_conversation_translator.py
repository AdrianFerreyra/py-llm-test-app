from src.application.dtos import LLMRequestDTO
from src.application.translators import conversation_to_llm_request
from src.domain import Conversation, LLMMessage, LLMToolCallMessage, UserMessage


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

    def test_transforms_tool_call_message_to_assistant_role(self):
        conversation = Conversation(messages=[
            LLMToolCallMessage(function_name="get_weather", arguments={"location": "London"}),
        ])

        result = conversation_to_llm_request(conversation)

        assert len(result.messages) == 1
        assert result.messages[0].role == "assistant"
        assert "get_weather" in result.messages[0].content
