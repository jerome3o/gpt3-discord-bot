from typing import Dict
from pydantic import BaseModel


class AiContext(BaseModel):
    identifier: str
    name: str
    situation_synopsis: str


class Summary(BaseModel):
    context_id: str
    summary: str
    opinions: Dict[str, str]


class Command(BaseModel):
    context_id: str
    sender_id: str
    sender_name: str
    content: str


class Message(BaseModel):
    sender_id: str
    sender_name: str
    content: str


class NameMap(BaseModel):
    context_id: str
    sender_id: str
    name: str
