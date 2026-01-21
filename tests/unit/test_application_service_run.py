from src.application import ApplicationService
from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMResponseDTO,
    LLMToolCallMessageDTO,
    LLMToolCallOutputMessageDTO,
    LLMToolCallResponseDTO,
    WeatherDTO,
)
from src.application.ports import InputPort, LLMPort, OutputPort, WeatherPort
from src.domain import (
    Conversation,
    LLMMessage,
    LLMToolCallMessage,
    ToolCallOutputMessage,
    UserMessage,
)


class FakeInputAdapter(InputPort):
    def __init__(self, inputs: list[str]):
        self.inputs = iter(inputs)

    def read(self) -> str:
        return next(self.inputs)


class FakeOutputAdapter(OutputPort):
    def __init__(self):
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)


class FakeLLMAdapter(LLMPort):
    def __init__(self, responses: list[LLMResponseDTO]):
        self.responses = iter(responses)
        self.calls: list[LLMRequestDTO] = []

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        self.calls.append(request)
        return next(self.responses)


class FakeWeatherAdapter(WeatherPort):
    def __init__(self, weather: WeatherDTO):
        self.weather = weather
        self.calls: list[str] = []

    def get_weather(self, location: str) -> WeatherDTO:
        self.calls.append(location)
        return self.weather


class TestApplicationServiceRun:
    def test_run_calls_llm_port_with_request_dto_and_outputs_message(self):
        fake_input = FakeInputAdapter(["Hello", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[LLMMessageResponseDTO(message="Hi there!")]
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert isinstance(fake_llm.calls[0], LLMRequestDTO)
        assert len(fake_llm.calls[0].messages) == 1
        assert fake_llm.calls[0].messages[0].role == "user"
        assert fake_llm.calls[0].messages[0].content == "Hello"
        assert fake_output.messages == ["Hi there!"]

    def test_run_sends_conversation_history_in_subsequent_calls(self):
        fake_input = FakeInputAdapter(["Hello", "How are you?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[
                LLMMessageResponseDTO(message="I'm an AI assistant."),
                LLMMessageResponseDTO(message="I'm doing well!"),
            ]
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 2

        # First call: just the first user message
        assert len(fake_llm.calls[0].messages) == 1
        assert fake_llm.calls[0].messages[0].role == "user"
        assert fake_llm.calls[0].messages[0].content == "Hello"

        # Second call: full conversation history
        assert len(fake_llm.calls[1].messages) == 3
        assert fake_llm.calls[1].messages[0].role == "user"
        assert fake_llm.calls[1].messages[0].content == "Hello"
        assert fake_llm.calls[1].messages[1].role == "assistant"
        assert fake_llm.calls[1].messages[1].content == "I'm an AI assistant."
        assert fake_llm.calls[1].messages[2].role == "user"
        assert fake_llm.calls[1].messages[2].content == "How are you?"

    def test_run_creates_conversation_with_user_and_llm_messages(self):
        fake_input = FakeInputAdapter(["Hello", "How are you?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[
                LLMMessageResponseDTO(message="Response 1"),
                LLMMessageResponseDTO(message="Response 2"),
            ]
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert app.conversation is not None
        assert isinstance(app.conversation, Conversation)
        assert len(app.conversation.messages) == 4

        assert isinstance(app.conversation.messages[0], UserMessage)
        assert app.conversation.messages[0].content == "Hello"

        assert isinstance(app.conversation.messages[1], LLMMessage)
        assert app.conversation.messages[1].content == "Response 1"

        assert isinstance(app.conversation.messages[2], UserMessage)
        assert app.conversation.messages[2].content == "How are you?"

        assert isinstance(app.conversation.messages[3], LLMMessage)
        assert app.conversation.messages[3].content == "Response 2"

    def test_run_exits_on_quit(self):
        fake_input = FakeInputAdapter(["Hello", "quit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[LLMMessageResponseDTO(message="Hi!")]
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert len(fake_output.messages) == 1

    def test_run_exits_on_q(self):
        fake_input = FakeInputAdapter(["Hello", "q"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[LLMMessageResponseDTO(message="Hi!")]
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
        )

        app.run()

        assert len(fake_llm.calls) == 1
        assert len(fake_output.messages) == 1

    def test_run_calls_weather_port_when_llm_requests_get_current_weather(self):
        fake_input = FakeInputAdapter(["What's the weather in London?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[
                LLMToolCallResponseDTO(
                    call_id="call_weather_1",
                    function_name="get_current_weather",
                    arguments={"location": "London"},
                ),
                LLMMessageResponseDTO(message="The weather in London is sunny, 20°C."),
            ]
        )
        fake_weather = FakeWeatherAdapter(
            weather=WeatherDTO(
                temperature_c=20.0,
                temperature_f=68.0,
                feels_like_c=19.0,
                feels_like_f=66.0,
                humidity=50,
                pressure_mb=1013.0,
                pressure_in=29.9,
                condition="Sunny",
                condition_icon="sunny.png",
                wind_mph=5.0,
                wind_kph=8.0,
                wind_direction="N",
                wind_degree=0,
                visibility_km=10.0,
                visibility_miles=6.0,
                uv_index=5.0,
                cloud_cover=10,
                last_updated="2024-01-01 12:00",
            )
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
            weather_port=fake_weather,
        )

        app.run()

        assert fake_weather.calls == ["London"]

    def test_run_sends_tool_call_result_back_to_llm(self):
        fake_input = FakeInputAdapter(["What's the weather in Paris?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[
                LLMToolCallResponseDTO(
                    call_id="call_weather_2",
                    function_name="get_current_weather",
                    arguments={"location": "Paris"},
                ),
                LLMMessageResponseDTO(message="It's sunny in Paris!"),
            ]
        )
        fake_weather = FakeWeatherAdapter(
            weather=WeatherDTO(
                temperature_c=25.0,
                temperature_f=77.0,
                feels_like_c=24.0,
                feels_like_f=75.0,
                humidity=40,
                pressure_mb=1015.0,
                pressure_in=30.0,
                condition="Sunny",
                condition_icon="sunny.png",
                wind_mph=3.0,
                wind_kph=5.0,
                wind_direction="W",
                wind_degree=270,
                visibility_km=15.0,
                visibility_miles=9.0,
                uv_index=7.0,
                cloud_cover=5,
                last_updated="2024-01-01 14:00",
            )
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
            weather_port=fake_weather,
        )

        app.run()

        # LLM should be called twice: first returns tool call, second returns message
        assert len(fake_llm.calls) == 2

        # Second call should include the tool call output in conversation
        second_call = fake_llm.calls[1]
        assert len(second_call.messages) == 3
        assert second_call.messages[0].role == "user"
        assert second_call.messages[0].content == "What's the weather in Paris?"
        # Second message should be the tool call DTO
        assert isinstance(second_call.messages[1], LLMToolCallMessageDTO)
        assert second_call.messages[1].call_id == "call_weather_2"
        assert second_call.messages[1].function_name == "get_current_weather"
        assert second_call.messages[1].arguments == {"location": "Paris"}
        # Third message should be the tool call output
        assert isinstance(second_call.messages[2], LLMToolCallOutputMessageDTO)
        assert second_call.messages[2].call_id == "call_weather_2"
        assert second_call.messages[2].output.temperature_c == 25.0
        assert second_call.messages[2].output.condition == "Sunny"

    def test_run_appends_tool_call_and_output_to_conversation(self):
        fake_input = FakeInputAdapter(["Weather in Tokyo?", "exit"])
        fake_output = FakeOutputAdapter()
        fake_llm = FakeLLMAdapter(
            responses=[
                LLMToolCallResponseDTO(
                    call_id="call_weather_3",
                    function_name="get_current_weather",
                    arguments={"location": "Tokyo"},
                ),
                LLMMessageResponseDTO(message="Tokyo weather is nice!"),
            ]
        )
        fake_weather = FakeWeatherAdapter(
            weather=WeatherDTO(
                temperature_c=22.0,
                temperature_f=72.0,
                feels_like_c=21.0,
                feels_like_f=70.0,
                humidity=60,
                pressure_mb=1010.0,
                pressure_in=29.8,
                condition="Partly cloudy",
                condition_icon="cloudy.png",
                wind_mph=10.0,
                wind_kph=16.0,
                wind_direction="E",
                wind_degree=90,
                visibility_km=12.0,
                visibility_miles=7.0,
                uv_index=4.0,
                cloud_cover=30,
                last_updated="2024-01-01 10:00",
            )
        )
        app = ApplicationService(
            input_port=fake_input,
            output_port=fake_output,
            llm_port=fake_llm,
            weather_port=fake_weather,
        )

        app.run()

        # Conversation should have: UserMessage, LLMToolCallMessage, ToolCallOutputMessage, LLMMessage
        assert len(app.conversation.messages) == 4
        assert isinstance(app.conversation.messages[0], UserMessage)
        assert isinstance(app.conversation.messages[1], LLMToolCallMessage)
        assert app.conversation.messages[1].call_id == "call_weather_3"
        assert app.conversation.messages[1].function_name == "get_current_weather"
        assert app.conversation.messages[1].arguments == {"location": "Tokyo"}
        assert isinstance(app.conversation.messages[2], ToolCallOutputMessage)
        assert app.conversation.messages[2].call_id == "call_weather_3"
        assert app.conversation.messages[2].output.temperature_c == 22.0
        assert isinstance(app.conversation.messages[3], LLMMessage)
        assert app.conversation.messages[3].content == "Tokyo weather is nice!"
