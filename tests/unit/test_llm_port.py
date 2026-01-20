from src.application.ports import LLMPort


class FakeLLMAdapter(LLMPort):
    def __init__(self, response: str):
        self.response = response
        self.calls: list[str] = []

    def call(self, message: str) -> str:
        self.calls.append(message)
        return self.response


class TestLLMPort:
    def test_call_receives_message_and_returns_response(self):
        adapter = FakeLLMAdapter(response="Hello, how can I help?")

        result = adapter.call("Hi there")

        assert result == "Hello, how can I help?"
        assert adapter.calls == ["Hi there"]
