from collections.abc import AsyncIterator

import pytest

from src.application.dtos import (
    LLMCompleted,
    LLMMessageChunk,
    LLMMessageResponseDTO,
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMStreamEvent,
    LLMToolCallResponseDTO,
)
from src.application.ports import LLMPort


class FakeStreamingLLMAdapter(LLMPort):
    def __init__(self, events: list[LLMStreamEvent]):
        self.events = events
        self.calls: list[LLMRequestDTO] = []

    async def call(self, request: LLMRequestDTO) -> AsyncIterator[LLMStreamEvent]:
        self.calls.append(request)
        for event in self.events:
            yield event


class TestLLMPortStreaming:
    @pytest.mark.asyncio
    async def test_call_yields_message_chunks(self):
        events = [
            LLMMessageChunk(content="Hello"),
            LLMMessageChunk(content=", "),
            LLMMessageChunk(content="world!"),
            LLMCompleted(final_response=LLMMessageResponseDTO(message="Hello, world!")),
        ]
        adapter = FakeStreamingLLMAdapter(events=events)
        request = LLMRequestDTO(
            messages=[LLMRequestMessageDTO(role="user", content="Hi")]
        )

        collected_events = []
        async for event in adapter.call(request):
            collected_events.append(event)

        assert len(collected_events) == 4
        assert isinstance(collected_events[0], LLMMessageChunk)
        assert collected_events[0].content == "Hello"
        assert isinstance(collected_events[1], LLMMessageChunk)
        assert collected_events[1].content == ", "
        assert isinstance(collected_events[2], LLMMessageChunk)
        assert collected_events[2].content == "world!"
        assert isinstance(collected_events[3], LLMCompleted)
        assert isinstance(collected_events[3].final_response, LLMMessageResponseDTO)
        assert collected_events[3].final_response.message == "Hello, world!"

    @pytest.mark.asyncio
    async def test_call_yields_completed_with_tool_call_response(self):
        events = [
            LLMCompleted(
                final_response=LLMToolCallResponseDTO(
                    call_id="call_abc123",
                    function_name="get_weather",
                    arguments={"location": "London"},
                )
            ),
        ]
        adapter = FakeStreamingLLMAdapter(events=events)
        request = LLMRequestDTO(
            messages=[
                LLMRequestMessageDTO(
                    role="user", content="What's the weather in London?"
                )
            ]
        )

        collected_events = []
        async for event in adapter.call(request):
            collected_events.append(event)

        assert len(collected_events) == 1
        assert isinstance(collected_events[0], LLMCompleted)
        assert isinstance(collected_events[0].final_response, LLMToolCallResponseDTO)
        assert collected_events[0].final_response.call_id == "call_abc123"
        assert collected_events[0].final_response.function_name == "get_weather"
        assert collected_events[0].final_response.arguments == {"location": "London"}
