from src.application.dtos import (
    LLMRequestDTO,
    LLMRequestMessageDTO,
    LLMToolCallMessageDTO,
    LLMToolCallOutputMessageDTO,
)
from src.domain import (
    Conversation,
    LLMMessage,
    LLMToolCallMessage,
    ToolCallOutputMessage,
    UserMessage,
)


def conversation_to_llm_request(conversation: Conversation) -> LLMRequestDTO:
    messages = []
    for message in conversation.messages:
        if isinstance(message, UserMessage):
            messages.append(LLMRequestMessageDTO(role="user", content=message.content))
        elif isinstance(message, LLMMessage):
            messages.append(
                LLMRequestMessageDTO(role="assistant", content=message.content)
            )
        elif isinstance(message, LLMToolCallMessage):
            messages.append(
                LLMToolCallMessageDTO(
                    call_id=message.call_id,
                    function_name=message.function_name,
                    arguments=message.arguments,
                )
            )
        elif isinstance(message, ToolCallOutputMessage):
            messages.append(
                LLMToolCallOutputMessageDTO(
                    call_id=message.call_id,
                    output=message.output,
                )
            )
    return LLMRequestDTO(messages=messages)
