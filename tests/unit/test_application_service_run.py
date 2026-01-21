from src.application import ApplicationService
from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMResponseDTO,
)
from src.application.ports import InputPort, LLMPort, OutputPort
from src.domain import Conversation, LLMMessage, UserMessage


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class FakeOutputAdapter(OutputPort):
    def __init__(self):
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)


class FakeLLMAdapter(LLMPort):
    def __init__(self, response: LLMResponseDTO):
        self.response = response
        self.calls: list[LLMRequestDTO] = []

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        self.calls.append(request)
        return self.response


class TestApplicationServiceRun:
    def test_run_calls_llm_port_with_request_dto_and_outputs_message(self):
        fake_input = FakeInputAdapter(["Hello", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            response=LLMMessageResponseDTO(message="Hi there!")
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert isinstance(fake_llm.calls[0], LLMRequestDTO)
        assert len(fake_llm.calls[0].messages) == 1
        assert fake_llm.calls[0].messages[0].role == "user"
        assert fake_llm.calls[0].messages[0].content == "Hello"
        assert fake_output.messages == ["Hi there!"]

    def test_run_sends_conversation_history_in_subsequent_calls(self):
        fake_input = FakeInputAdapter(["Hello", "How are you?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            response=LLMMessageResponseDTO(message="I'm an AI assistant.")
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 2

        # First call: just the first user message
        assert len(fake_llm.calls[0].messages) == 1
        assert fake_llm.calls[0].messages[0].role == "user"
        assert fake_llm.calls[0].messages[0].content == "Hello"

        # Second call: full conversation history
        assert len(fake_llm.calls[1].messages) == 3
        assert fake_llm.calls[1].messages[0].role == "user"
        assert fake_llm.calls[1].messages[0].content == "Hello"
        assert fake_llm.calls[1].messages[1].role == "assistant"
        assert fake_llm.calls[1].messages[1].content == "I'm an AI assistant."
        assert fake_llm.calls[1].messages[2].role == "user"
        assert fake_llm.calls[1].messages[2].content == "How are you?"

    def test_run_creates_conversation_with_user_and_llm_messages(self):
        fake_input = FakeInputAdapter(["Hello", "How are you?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            response=LLMMessageResponseDTO(message="Response")
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert app.conversation is not None
        assert isinstance(app.conversation, Conversation)
        assert len(app.conversation.messages) == 4

        assert isinstance(app.conversation.messages[0], UserMessage)
        assert app.conversation.messages[0].content == "Hello"

        assert isinstance(app.conversation.messages[1], LLMMessage)
        assert app.conversation.messages[1].content == "Response"

        assert isinstance(app.conversation.messages[2], UserMessage)
        assert app.conversation.messages[2].content == "How are you?"

        assert isinstance(app.conversation.messages[3], LLMMessage)
        assert app.conversation.messages[3].content == "Response"

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["Hello", "quit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            response=LLMMessageResponseDTO(message="Hi!")
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert len(fake_output.messages) == 1

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["Hello", "q"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            response=LLMMessageResponseDTO(message="Hi!")
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert len(fake_output.messages) == 1
