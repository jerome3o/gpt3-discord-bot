from typing import Dict
from pydantic import BaseModel, Field


class TimestampedItem(BaseModel):
    timestamp: float


class AiContext(BaseModel):
    context_id: str
    # TODO: not sure what else might have to live here?


class Summary(TimestampedItem):
    context_id: str
    summary: str
    opinions: Dict[str, str] = Field(default_factory=dict)


class Command(TimestampedItem):
    context_id: str
    sender_id: str
    sender_name: str
    content: str


class Message(TimestampedItem):
    sender_id: str
    sender_name: str
    content: str


class NameMap(TimestampedItem):
    context_id: str
    sender_id: str
    name: str
