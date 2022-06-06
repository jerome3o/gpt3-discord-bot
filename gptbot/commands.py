from typing import Callable, List
import discord

from gptbot.db import get_latest_name_map, set_name_map


MessageHandler = Callable[[str, discord.Message, List[str]], str]


def human_name_handler(
    context_id: str, message: discord.Message, tokens: List[str]
) -> str:
    sender_id = message.author.name

    if len(tokens) == 1:
        name_map = get_latest_name_map(context_id=context_id, sender_id=sender_id)
        name = name_map.name if name_map else sender_id
        return f"Current name for {sender_id}: {name}"

    new_name = " ".join(tokens[1:])
    name_map = set_name_map(
        context_id=context_id,
        sender_id=sender_id,
        new_name=new_name,
    )
    return f"Set name of {sender_id} to: {new_name}"
