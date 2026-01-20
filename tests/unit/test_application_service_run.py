from src.application import ApplicationService
from src.application.ports import InputPort, OutputPort


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


class TestApplicationServiceRun:
    def test_run_reads_from_input_port_and_echoes_response(self):
        fake_input = FakeInputAdapter(["hello", "world", "exit"])
        fake_output = FakeOutputAdapter()
        app = ApplicationService(input_port=fake_input, output_port=fake_output)

        app.run()

        assert "hello" in fake_output.messages
        assert "world" in fake_output.messages

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["hello", "quit"])
        fake_output = FakeOutputAdapter()
        app = ApplicationService(input_port=fake_input, output_port=fake_output)

        app.run()

        assert "hello" in fake_output.messages
        assert "quit" not in fake_output.messages

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["test", "q"])
        fake_output = FakeOutputAdapter()
        app = ApplicationService(input_port=fake_input, output_port=fake_output)

        app.run()

        assert "test" in fake_output.messages
        assert "q" not in fake_output.messages
