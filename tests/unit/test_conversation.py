from src.domain import Conversation, LLMMessage, UserMessage


class TestConversation:
    def test_stores_ordered_list_of_messages(self):
        messages = [
            UserMessage(content="Hello"),
            LLMMessage(content="Hi there!"),
            UserMessage(content="How are you?"),
        ]
        conversation = Conversation(messages=messages)

        assert conversation.messages == messages
        assert len(conversation.messages) == 3
        assert conversation.messages[0].content == "Hello"
        assert conversation.messages[1].content == "Hi there!"
        assert conversation.messages[2].content == "How are you?"

    def test_empty_conversation(self):
        conversation = Conversation(messages=[])

        assert conversation.messages == []
        assert len(conversation.messages) == 0

    def test_preserves_message_order(self):
        msg1 = UserMessage(content="First")
        msg2 = LLMMessage(content="Second")
        msg3 = UserMessage(content="Third")

        conversation = Conversation(messages=[msg1, msg2, msg3])

        assert conversation.messages[0] is msg1
        assert conversation.messages[1] is msg2
        assert conversation.messages[2] is msg3
