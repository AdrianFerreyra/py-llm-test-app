from src.application.ports import OutputPort


class StdOutOutputAdapter(OutputPort):
    def write(self, message: str) -> None:
        print(message)
