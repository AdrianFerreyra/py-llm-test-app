from dataclasses import dataclass


@dataclass
class LLMResponseDTO:
    pass


@dataclass
class LLMMessageResponseDTO(LLMResponseDTO):
    message: str


@dataclass
class LLMToolCallResponseDTO(LLMResponseDTO):
    call_id: str
    function_name: str
    arguments: dict[str, str]


@dataclass
class LLMStreamEvent:
    pass


@dataclass
class LLMMessageChunk(LLMStreamEvent):
    content: str


@dataclass
class LLMCompleted(LLMStreamEvent):
    final_response: "LLMResponseDTO"