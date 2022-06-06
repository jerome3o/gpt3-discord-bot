import os
import openai

import discord

from gptbot.helpers import get_context_id_from_message
from gptbot.db import get_context_from_id
from gptbot.commands import human_name_handler, COMMANDS


openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.environ.get("DISCORD_API_KEY")


client = discord.Client()

MESSAGE_BUFFER_SIZE = 5
CLEAR = "$clear"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if not message.channel.name.startswith("story-ai-"):
        return

    context_id = get_context_id_from_message(message)
    context = get_context_from_id(context_id=context_id)

    a: str = "ge"

    tokens = message.content.split()
    if tokens[0] in COMMANDS:
        await message.channel.send(COMMANDS[tokens[0]](context_id, message, tokens))
        return

    print(context)

    await message.channel.send(context_id)


client.run(API_KEY)
