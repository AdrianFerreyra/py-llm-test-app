from abc import ABC
from dataclasses import dataclass

from .weather_info import WeatherInfo


@dataclass
class Message(ABC):
    pass


@dataclass
class UserMessage(Message):
    content: str


@dataclass
class LLMMessage(Message):
    content: str


@dataclass
class LLMToolCallMessage(Message):
    call_id: str
    function_name: str
    arguments: dict[str, str]


@dataclass
class ToolCallOutputMessage(Message):
    call_id: str
    output: WeatherInfo
