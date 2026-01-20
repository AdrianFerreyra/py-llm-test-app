from src.application import ApplicationService
from src.application.dtos import LLMMessageResponseDTO, LLMResponseDTO
from src.application.ports import InputPort, LLMPort, OutputPort


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
    def __init__(self, responses: dict[str, LLMResponseDTO]):
        self.responses = responses
        self.calls: list[str] = []

    def call(self, message: str) -> LLMResponseDTO:
        self.calls.append(message)
        return self.responses.get(
            message, LLMMessageResponseDTO(message="I don't understand.")
        )


class TestApplicationServiceRun:
    def test_run_calls_llm_port_with_user_input_and_outputs_message(self):
        fake_input = FakeInputAdapter(["Hello", "How are you?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter({
            "Hello": LLMMessageResponseDTO(message="Hi there! How can I help you?"),
            "How are you?": LLMMessageResponseDTO(message="I'm doing well, thank you!"),
        })
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert fake_llm.calls == ["Hello", "How are you?"]
        assert len(fake_output.messages) == 2
        assert fake_output.messages[0] == "Hi there! How can I help you?"
        assert fake_output.messages[1] == "I'm doing well, thank you!"

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["Hello", "quit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter({
            "Hello": LLMMessageResponseDTO(message="Hi!"),
        })
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert fake_llm.calls == ["Hello"]
        assert len(fake_output.messages) == 1

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["Hello", "q"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter({
            "Hello": LLMMessageResponseDTO(message="Hi!"),
        })
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert fake_llm.calls == ["Hello"]
        assert len(fake_output.messages) == 1
