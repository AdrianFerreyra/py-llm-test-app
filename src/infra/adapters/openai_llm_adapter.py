import dataclasses
import json
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from src.application.dtos import (
    LLMCompleted,
    LLMMessageChunk,
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMStreamEvent,
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
        self.client = AsyncOpenAI(api_key=api_key)

    async def call(self, request: LLMRequestDTO) -> AsyncIterator[LLMStreamEvent]:
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

        stream = await self.client.responses.create(
            model="gpt-4.1",
            input=messages,
            tools=self.available_tools,
            stream=True,
        )

        async for event in stream:
            if event.type == "response.output_text.delta":
                yield LLMMessageChunk(content=event.delta)
            elif event.type == "response.output_item.done":
                if event.item.type == "function_call":
                    yield LLMCompleted(
                        final_response=LLMToolCallResponseDTO(
                            call_id=event.item.call_id,
                            function_name=event.item.name,
                            arguments=json.loads(event.item.arguments),
                        )
                    )
                elif event.item.type == "message":
                    full_text = "".join(
                        content.text for content in event.item.content
                    )
                    yield LLMCompleted(
                        final_response=LLMMessageResponseDTO(message=full_text)
                    )
