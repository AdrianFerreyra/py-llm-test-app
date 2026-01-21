from src.application.ports import OutputPort


class StdOutOutputAdapter(OutputPort):
    async def write(self, message: str) -> None:
        print(message, end="", flush=True)

    def flush(self) -> None:
        print()
