from openai import OpenAI

from src.application.dtos import LLMMessageResponseDTO, LLMRequestDTO, LLMResponseDTO
from src.application.ports import LLMPort


class OpenAILLMAdapter(LLMPort):
    available_tools = [
        {
            "type": "function",
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. London"
                    },
                },
                "required": ["location"],
                "additionalProperties": False
            },
            "strict": True
        }
    ]
        
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]
        response = self.client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=self.tools,
        )
        return LLMMessageResponseDTO(message=response.output_text)
