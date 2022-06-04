import os
import openai

from discord import Message, Client
from gptbot.legacy.model import PromptConfig


openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.environ.get("DISCORD_API_KEY")


client = Client()

MESSAGE_BUFFER_SIZE = 5
CLEAR = "$clear"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if not message.channel.name.startswith("ai-"):
        return

    if message.channel.name == "ai-consciousness":
        return

    if message.content == CLEAR:
        return

    try:
        config = PromptConfig.parse_raw(message.channel.topic)
    except Exception:
        await message.channel.send("Invalid config!!")
        return

    raw_messages = await message.channel.history(limit=MESSAGE_BUFFER_SIZE).flatten()
    messages = []
    for m in raw_messages:
        if m.content == CLEAR:
            break
        messages.append(m)

    s = "\n".join(
        f"{config.ai_name if m.author == client.user else config.human_name}: {m.content}"
        for m in messages[::-1]
    )

    prompt = f"{config.prompt}\n\n{s}\n{config.ai_name}: "

    if message.content == "$prompt":
        await message.channel.send(prompt)
        return

    # if not message.content.endswith("?"):
    #     return

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, temperature=0.6, max_tokens=300
    )
    print()

    await message.channel.send(response.choices[0].text)


client.run(API_KEY)
