from dataclasses import dataclass

from .message import Message


@dataclass
class Conversation:
    messages: list[Message]
