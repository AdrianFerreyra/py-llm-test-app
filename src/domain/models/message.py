from abc import ABC
from dataclasses import dataclass


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
    function_name: str
    arguments: dict[str, str]
