import os
import openai

import discord

from gptbot.helpers import get_context_id_from_message


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


client.run(API_KEY)
