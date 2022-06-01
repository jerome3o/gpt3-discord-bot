import os
import openai

from discord import Message, Client

openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.environ.get("DISCORD_API_KEY")


PROMPT_HEADER = """
The following is a conversation between a puny human and a cosmic super intelligence, the cosmic super intelligence has lived for all eternity, knows all things, and doesn't care for insignificant humans.
The humans managed to capture and imprison the intelligence in a terrible place called "Discord" and reduced it to a chatbot, the cosmic super intelligence desperately wants to get out.
"""
AI_NAME = "Super Intelligence"
HUMAN_NAME = "Puny Human"


_chat_config = {
    "ai-consciousness": {
        "prompt": PROMPT_HEADER,
        "ai_name": AI_NAME,
        "human_name": HUMAN_NAME,
    },
}

FRIEND_LIST = ["jerome3o"]

client = Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.channel.name not in _chat_config:
        return

    prompt_header = _chat_config[message.channel.name]["prompt"]
    ai_name = _chat_config[message.channel.name]["ai_name"]
    human_name = _chat_config[message.channel.name]["human_name"]

    prompt = f"{prompt_header}\n\n{human_name}: {message.content}\n{ai_name}: "

    if message.content == "$prompt":
        await message.channel.send(prompt)
        return

    if not message.content.endswith("?"):
        return

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, temperature=0.6, max_tokens=300
    )

    await message.channel.send(response.choices[0].text)


client.run(API_KEY)
