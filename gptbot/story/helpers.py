from typing import List

import discord
from gptbot.model import Dialog


def get_context_id_from_message(message: discord.Message):
    channel: discord.TextChannel = message.channel
    channel_name = channel.name
    guild_name = message.guild.name
    guild_id = message.guild.id

    return f"{channel_name}_{guild_name}_{guild_id}"

    # TODO: get identifier for discord server
    # server_name = channel.


def dialog_list_to_string(dialog: List[Dialog]) -> str:
    return "\n".join([f"{d.sender_name}: {d.content}" for d in dialog])
