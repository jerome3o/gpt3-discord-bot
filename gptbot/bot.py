import os
import openai
import logging

import discord

from gptbot.helpers import dialog_list_to_string, get_context_id_from_message
from gptbot.db import (
    add_dialog,
    get_latest_name_map,
)
from gptbot.prompt import construct_prompt
from gptbot.commands import COMMANDS
from gptbot.model import AI_SENDER_ID, Dialog


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

    # Handle commands

    if message.content.startswith("$"):
        tokens = message.content.split()
        if tokens[0] in COMMANDS:
            await message.channel.send(COMMANDS[tokens[0]](context_id, message, tokens))
            return
        await message.channel.send(f"Unknown command")
        return

    # Handle dialog

    add_dialog(
        Dialog(
            sender_id=message.author.name,
            sender_name=get_latest_name_map(
                context_id=context_id, sender_id=message.author.name
            ).name,
            context_id=context_id,
            content=message.content,
        )
    )

    # Construct Prompt
    prompt = construct_prompt(context_id, add_ai_prompt=True)
    if message.content == "$prompt":
        await message.channel.send(prompt)
        return


def main():
    client.run(API_KEY)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
