from src.application.dtos import LLMMessageResponseDTO, LLMToolCallResponseDTO
from src.application.ports import InputPort, LLMPort, OutputPort, WeatherPort
from src.application.translators import (
    conversation_to_llm_request,
    weather_dto_to_info,
)
from src.domain import (
    Conversation,
    LLMMessage,
    LLMToolCallMessage,
    ToolCallOutputMessage,
    UserMessage,
)


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

            response = self._call_llm()

            if isinstance(response, LLMToolCallResponseDTO):
                response = self._handle_tool_call(response)

            if isinstance(response, LLMMessageResponseDTO):
                self.conversation.messages.append(LLMMessage(content=response.message))
                self.output_port.write(response.message)

    def _call_llm(self):
        request = conversation_to_llm_request(self.conversation)
        return self.llm_port.call(request)

    def _handle_tool_call(self, response: LLMToolCallResponseDTO):
        self.conversation.messages.append(
            LLMToolCallMessage(
                call_id=response.call_id,
                function_name=response.function_name,
                arguments=response.arguments,
            )
        )

        if response.function_name == "get_current_weather":
            weather_dto = self.weather_port.get_weather(response.arguments["location"])
            weather_info = weather_dto_to_info(weather_dto)
            self.conversation.messages.append(
                ToolCallOutputMessage(
                    call_id=response.call_id,
                    output=weather_info,
                )
            )

        return self._call_llm()
