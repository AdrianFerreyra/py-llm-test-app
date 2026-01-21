from src.application.dtos import LLMRequestDTO, LLMRequestMessageDTO
from src.domain import Conversation, LLMMessage, LLMToolCallMessage, UserMessage


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
                LLMRequestMessageDTO(
                    role="assistant", content=f"Tool call: {message.function_name}"
                )
            )
    return LLMRequestDTO(messages=messages)
