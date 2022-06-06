import time
from typing import Dict
from pydantic import BaseModel, Field


AI_SENDER_ID = "AI"


class TimestampedItem(BaseModel):
    timestamp: float = Field(default_factory=time.time)


class AiContext(BaseModel):
    context_id: str
    # TODO: not sure what else might have to live here?


class Summary(TimestampedItem):
    context_id: str
    summary: str
    opinions: Dict[str, str] = Field(default_factory=dict)


class Action(TimestampedItem):
    context_id: str
    sender_id: str
    sender_name: str
    content: str


class Dialog(TimestampedItem):
    context_id: str
    sender_id: str
    sender_name: str
    content: str


class NameMap(TimestampedItem):
    context_id: str
    sender_id: str
    name: str
