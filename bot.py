import os
from discord import Message, Client

API_KEY = os.environ.get("DISCORD_API_KEY")

NICE_PROMPT_HEADER = "The following is a conversation with an AI assistant. The assistant is helpf"\
    "ul, creative, clever, and very friendly."

client = Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    async for message in message.channel.history():
        print(message)


client.run(API_KEY)
