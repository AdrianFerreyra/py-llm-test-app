from io import StringIO
from unittest.mock import patch

from src.infra import StdOutOutputAdapter
from src.application.ports import OutputPort


class TestStdOutOutputAdapter:
    def test_write_prints_to_stdout(self):
        adapter = StdOutOutputAdapter()
        output_stream = StringIO()

        with patch("sys.stdout", output_stream):
            adapter.write("hello world")

        assert output_stream.getvalue() == "hello world\n"
