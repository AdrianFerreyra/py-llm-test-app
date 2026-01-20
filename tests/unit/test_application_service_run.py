from io import StringIO
from unittest.mock import patch

from src.application import ApplicationService


class TestApplicationServiceRun:
    def test_run_reads_from_stdin_and_echoes_response(self):
        app = ApplicationService()

        user_inputs = ["hello", "world", "exit"]
        input_stream = StringIO("\n".join(user_inputs) + "\n")
        output_stream = StringIO()

        with patch("sys.stdin", input_stream), patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "hello" in output
        assert "world" in output

    def test_run_exits_on_quit(self):
        app = ApplicationService()

        user_inputs = ["hello", "quit"]
        input_stream = StringIO("\n".join(user_inputs) + "\n")
        output_stream = StringIO()

        with patch("sys.stdin", input_stream), patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "hello" in output
        assert "quit" not in output

    def test_run_exits_on_q(self):
        app = ApplicationService()

        user_inputs = ["test", "q"]
        input_stream = StringIO("\n".join(user_inputs) + "\n")
        output_stream = StringIO()

        with patch("sys.stdin", input_stream), patch("sys.stdout", output_stream):
            app.run()

        output = output_stream.getvalue()
        assert "test" in output
        assert output.count("q") == 0 or "q" not in output.split()
