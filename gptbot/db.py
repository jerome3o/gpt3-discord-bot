import time
import os
import logging
from functools import wraps
from bson.objectid import ObjectId
from typing import List, Optional, Type, TypeVar, Callable, Union
from pydantic import BaseModel, parse_obj_as
from pymongo import MongoClient
from pymongo.collection import Collection

from gptbot.model import AI_SENDER_ID, AiContext, NameMap, Summary, Dialog

_logger = logging.getLogger(__name__)

CON_STR = os.environ["MONGO_CONNECTION_STRING"]
client = MongoClient(CON_STR)

DB_NAME = "story_bot"

Func = TypeVar("Func", bound=Callable)
PrimitiveType = TypeVar("PrimitiveType", bound=Union[dict, list, str, int, float])


def _output_as(model: Type):
    def _decorator(f: Func) -> Func:
        @wraps(f)
        def _wrapper(*args, **kwargs):
            output = _id_to_str(f(*args, **kwargs))
            if output is None:
                return output
            return parse_obj_as(model, output)

        return _wrapper

    return _decorator


def _id_to_str(value: PrimitiveType) -> PrimitiveType:
    # todo this should be done better, maybe db side? maybe pydantic validation side?
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, dict):
        return {k: _id_to_str(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_id_to_str(v) for v in value]

    return value


def get_collection(model: Type[BaseModel]) -> Collection:
    return client[DB_NAME].get_collection(model.__name__)


@_output_as(AiContext)
def get_context_from_id(context_id: str) -> AiContext:
    col = get_collection(AiContext)
    for value in col.find({"context_id": context_id}):
        return value

    value = col.insert_one(AiContext(context_id=context_id).dict())
    return col.find_one({"_id": value.inserted_id})


@_output_as(List[NameMap])
def get_name_maps(context_id: str, sender_id: str) -> List[NameMap]:
    col = get_collection(NameMap)
    return list(col.find({"context_id": context_id, "sender_id": sender_id}))


def get_latest_name_map(context_id: str, sender_id: str) -> Optional[NameMap]:
    name_maps = get_name_maps(context_id=context_id, sender_id=sender_id)

    if not name_maps:
        return None

    return max(
        name_maps,
        key=lambda m: m.timestamp,
    )


@_output_as(NameMap)
def set_name_map(context_id: str, sender_id: str, new_name: str) -> NameMap:
    # TODO(j.swannack): Should this be constructed in external to this function?
    name_map = NameMap(
        context_id=context_id,
        sender_id=sender_id,
        name=new_name,
        timestamp=time.time(),
    )
    _logger.info(f"Adding name map: {name_map}")
    col = get_collection(NameMap)
    v = col.insert_one(name_map.dict())
    return col.find_one({"_id": v.inserted_id})


@_output_as(List[Summary])
def get_summaries(context_id: str) -> List[Summary]:
    col = get_collection(Summary)
    return list(col.find({"context_id": context_id}))


def get_latest_summary(context_id: str) -> Summary:
    summaries = get_summaries(context_id=context_id)
    if not summaries:
        return None
    return max(summaries, key=lambda s: s.timestamp)


@_output_as(Summary)
def add_summary(summary: Summary):
    _logger.info(f"Adding summary: {summary}")
    col = get_collection(Summary)
    v = col.insert_one(summary.dict())
    return col.find_one({"_id": v.inserted_id})


@_output_as(Dialog)
def add_dialog(dialog: Dialog):
    _logger.info(f"Adding dialog: {dialog}")
    col = get_collection(Dialog)
    v = col.insert_one(dialog.dict())
    return col.find_one(v.inserted_id)


@_output_as(List[Dialog])
def get_dialog_since(context_id: str, timestamp: float):
    col = get_collection(Dialog)
    return list(col.find({"context_id": context_id, "timestamp": {"$gte": timestamp}}))


@_output_as(NameMap)
def get_latest_ai_name_map(context_id: str) -> NameMap:
    return get_latest_name_map(context_id, sender_id=AI_SENDER_ID)


def get_latest_ai_name(context_id: str) -> str:
    name_map = get_latest_ai_name_map(context_id)
    return name_map.name if name_map else AI_SENDER_ID
