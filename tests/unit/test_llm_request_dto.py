from src.application.dtos import LLMRequestDTO, LLMRequestMessageDTO


class TestLLMRequestMessageDTO:
    def test_stores_role_and_content(self):
        message = LLMRequestMessageDTO(role="user", content="Hello!")

        assert message.role == "user"
        assert message.content == "Hello!"


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
