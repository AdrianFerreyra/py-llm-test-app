from dataclasses import dataclass


@dataclass
class LLMResponseDTO:
    pass


@dataclass
class LLMMessageResponseDTO(LLMResponseDTO):
    message: str


@dataclass
class LLMToolCallResponseDTO(LLMResponseDTO):
    function_name: str
    arguments: dict[str, str]
