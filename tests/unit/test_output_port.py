from io import StringIO
from unittest.mock import patch

import pytest

from src.infra import StdOutOutputAdapter
from src.application.ports import OutputPort


class TestStdOutOutputAdapter:
    @pytest.mark.asyncio
    async def test_write_prints_to_stdout_without_newline(self):
        adapter = StdOutOutputAdapter()
        output_stream = StringIO()

        with patch("sys.stdout", output_stream):
            await adapter.write("hello world")

        assert output_stream.getvalue() == "hello world"
