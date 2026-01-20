from unittest.mock import patch

from src.infra import StdInInputAdapter
from src.application.ports import InputPort


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class TestStdInInputAdapter:
    def test_read_returns_user_input(self):
        with patch("builtins.input", return_value="hello world"):
            adapter = StdInInputAdapter()
            result = adapter.read()

        assert result == "hello world"
