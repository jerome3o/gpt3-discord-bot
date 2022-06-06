from typing import Callable, List
import discord
import json
import time

from gptbot.db import get_latest_name_map, get_latest_summary, set_name_map, add_summary
from gptbot.model import AI_SENDER_ID, Summary


MessageHandler = Callable[[str, discord.Message, List[str]], str]

_SUMMARY_HELP = """No summary has been set, to set one, use:
$summary
```
{
  "summary": "This is a converation between XYZ",
  "opinions": {
    "character X": "Character X is my friend, I can trust them",
    "character Y": "Character Y is my enemy, I want to kill them"
  }
}
```
"""


def human_name_handler(
    context_id: str, message: discord.Message, tokens: List[str]
) -> str:
    return _name_handler(
        context_id=context_id, sender_id=message.author.name, tokens=tokens
    )


def ai_name_handler(
    context_id: str, message: discord.Message, tokens: List[str]
) -> str:
    return _name_handler(context_id=context_id, sender_id=AI_SENDER_ID, tokens=tokens)


def _name_handler(context_id: str, sender_id: str, tokens: List[str]):

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


def summary_handler(context_id: str, message: discord.Message, tokens: List[str]):
    if len(tokens) == 1:
        summary = get_latest_summary(context_id)
        if summary is None:
            return _SUMMARY_HELP
    else:
        config = message.content.replace("$summary", "").replace("```", "")
        partial = json.loads(config)
        summary = add_summary(
            summary=Summary(
                **partial,
                timestamp=time.time(),
                context_id=context_id,
            ),
        )

    return f"Current summary: \n```{summary.json(indent=4)}```"


COMMANDS = {
    "$name": human_name_handler,
    "$ainame": ai_name_handler,
    "$summary": summary_handler,
}
