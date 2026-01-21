import dataclasses
import json

from openai import OpenAI

from src.application.dtos import (
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMResponseDTO,
    LLMToolCallMessageDTO,
    LLMToolCallOutputMessageDTO,
    LLMToolCallResponseDTO,
)
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
                        "description": "City name, e.g. London",
                    },
                },
                "required": ["location"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    ]

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def call(self, request: LLMRequestDTO) -> LLMResponseDTO:
        messages = []
        for msg in request.messages:
            if isinstance(msg, LLMToolCallMessageDTO):
                messages.append(
                    {
                        "type": "function_call",
                        "call_id": msg.call_id,
                        "name": msg.function_name,
                        "arguments": json.dumps(msg.arguments),
                    }
                )
            elif isinstance(msg, LLMToolCallOutputMessageDTO):
                messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": msg.call_id,
                        "output": json.dumps(dataclasses.asdict(msg.output)),
                    }
                )
            else:
                messages.append({"role": msg.role, "content": msg.content})

        response = self.client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=self.available_tools,
        )

        for output_item in response.output:
            if output_item.type == "function_call":
                return LLMToolCallResponseDTO(
                    call_id=output_item.call_id,
                    function_name=output_item.name,
                    arguments=json.loads(output_item.arguments),
                )

        return LLMMessageResponseDTO(message=response.output_text)
