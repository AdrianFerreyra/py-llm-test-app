from dataclasses import dataclass


@dataclass
class LLMRequestMessageDTO:
    role: str
    content: str


@dataclass
class LLMRequestDTO:
    messages: list[LLMRequestMessageDTO]
