from typing import Callable, List
import discord

from gptbot.db import get_latest_name_map


MessageHandler = Callable[[str, discord.Message, List[str]], str]


def human_name_handler(
    context_id: str, message: discord.Message, tokens: List[str]
) -> str:
    if len(tokens) == 1:
        name_map = get_latest_name_map(
            context_id=context_id, sender_id=message.author.name
        )
        return name_map.name if name_map else message.author.name
