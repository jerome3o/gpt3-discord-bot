import os
from pymongo import MongoClient

from gptbot.model import AiContext

CON_STR = os.environ("MONGO_CONNECTION_STRING")
client = MongoClient(CON_STR)

_DEFAULT_AI_CONTEXT = AiContext(
    identifier="",
    name="AI",
    situation_synopsis="An AI talks to a human for the first time",
)
