from dataclasses import dataclass, field

from src.domain import WeatherInfo


@dataclass
class LLMRequestMessageDTO:
    role: str = ""
    content: str = ""


@dataclass
class LLMToolCallMessageDTO(LLMRequestMessageDTO):
    call_id: str = ""
    function_name: str = ""
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass
class LLMToolCallOutputMessageDTO(LLMRequestMessageDTO):
    call_id: str = ""
    output: WeatherInfo | None = None


@dataclass
class LLMRequestDTO:
    messages: list[LLMRequestMessageDTO] = field(default_factory=list)
