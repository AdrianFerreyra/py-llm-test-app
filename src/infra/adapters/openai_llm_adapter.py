from openai import OpenAI

from src.application.dtos import LLMMessageResponseDTO, LLMRequestDTO, LLMResponseDTO
from src.application.ports import LLMPort


class OpenAILLMAdapter(LLMPort):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]
        response = self.client.responses.create(
            model="gpt-4.1",
            input=messages,
        )
        return LLMMessageResponseDTO(message=response.output_text)
