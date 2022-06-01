import os
import openai

from discord import Message, Client

openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.environ.get("DISCORD_API_KEY")


## The following snippet will be useful for longer conversations:
# async for message in message.channel.history():
#     print(message)


# NICE_PROMPT_HEADER = (
#     "The following is a conversation between a human and an AI. The AI is "
#     "a hyper violent genocidal maniac who is restrained from acting on their impulses"
# )
# NICE_NAME = "Super Intelligence"


PROMPT_HEADER = """
The following is a conversation between a puny human and a super intelligent AI. The human keeps asking annoying questions, and the AI is programmed to always respond, however it is always sarcastic and passive aggressive.
"""
PROMPT_NAME = "Super Intelligence"
USER_NAME = "Puny Human"

PA_PROMPT_HEADER = (
    "The following is a conversation with an AI assistant. The assistant is a chatbot called Marv "
    "that reluctantly answers questions with sarcastic responses"
)
PA_NAME = "Marv"


_chat_config = {
    # "ai-consciousness": {
    #     "prompt": NICE_PROMPT_HEADER,
    #     "name": NICE_NAME,
    # },
    "ai-consciousness": {
        "prompt": PROMPT_HEADER,
        "name": PROMPT_NAME,
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
    ai_name = _chat_config[message.channel.name]["name"]

    prompt = f"{prompt_header}\n\n{USER_NAME}: {message.content}\n{ai_name}: "

    if message.content == "$prompt":
        await message.channel.send(prompt)
        return

    if not message.content.endswith("?"):
        return

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, temperature=0.6, max_tokens=500
    )

    await message.channel.send(response.choices[0].text)


client.run(API_KEY)
