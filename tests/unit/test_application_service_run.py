from io import StringIO
from unittest.mock import patch

from src.application import ApplicationService
from src.application.ports import InputPort


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class TestApplicationServiceRun:
    def test_run_reads_from_input_port_and_echoes_response(self):
        fake_input = FakeInputAdapter(["hello", "world", "exit"])
        app = ApplicationService(input_port=fake_input)

        output_stream = StringIO()
        with patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "hello" in output
        assert "world" in output

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["hello", "quit"])
        app = ApplicationService(input_port=fake_input)

        output_stream = StringIO()
        with patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "hello" in output
        assert "quit" not in output

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["test", "q"])
        app = ApplicationService(input_port=fake_input)

        output_stream = StringIO()
        with patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "test" in output
        assert "q" not in output.split()
