from src.application.dtos import LLMMessageResponseDTO
from src.application.ports import InputPort, LLMPort, OutputPort, WeatherPort
from src.domain import Conversation, LLMMessage, UserMessage


class ApplicationService:
    def __init__(
        self,
        input_port: InputPort | None = None,
        output_port: OutputPort | None = None,
        llm_port: LLMPort | None = None,
        weather_port: WeatherPort | None = None,
    ):
        self.input_port = input_port
        self.output_port = output_port
        self.llm_port = llm_port
        self.weather_port = weather_port
        self.conversation: Conversation | None = None

    def run(self) -> None:
        self.conversation = Conversation(messages=[])

        while True:
            user_input = self.input_port.read()
            if not user_input:
                break
            message = user_input.rstrip()
            if message in ("quit", "exit", "q"):
                break

            self.conversation.messages.append(UserMessage(content=message))

            response = self.llm_port.call(message)
            if isinstance(response, LLMMessageResponseDTO):
                self.conversation.messages.append(LLMMessage(content=response.message))
                self.output_port.write(response.message)
