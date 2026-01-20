from src.application.ports import InputPort


class StdInInputAdapter(InputPort):
    def read(self) -> str:
        return input("> ")
