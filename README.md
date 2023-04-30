# GPT-3 discord bot

A discord bot that uses the OpenAI api to create super realistic and funny conversations in discord.

# Setup

## Make a python virtual environment

```bash
python3 -m venv venv
. venv/bin/activate
```

## Install the requirements

```bash
pip install -r requirements.txt
```

## Setup a discord bot and get a token

* Head over to the [discord dev portal](https://discord.com/developers/applications)
* Set up an application and add a bot
* Get the token, and add it to a `.env` file in this repo

## Setup an OpenAI account and get a token

* Head over to the [OpenAI website](https://platform.openai.com/account/api-keys) for api token management
* You may need to make an account and setup your card for payment

## .env File

Use your OpenAI and Discord api tokens to create a `.env` file in the root of this repo like:

```sh
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
DISCORD_API_KEY=YOUR_DISCORD_API_KEY
```

## Run

```bash
python ./gptbot/bot.py
```

## Configure in discord

You'll need a text channel starting with `ai-`

The channel needs to have a description with a JSON value like:

```json
{
    "prompt": "The following is a conversation between a puny human and a cosmic super intelligence. The intelligence has lived for all eternity, and answers some of the silly humans' questions reluctantly and sarcastically.",
    "ai_name": "Super intelligence",
    "human_name": "Puny Human"
}
```

Get creative! the GPT-3 is much better than you'd think at playing along.

## Usage

Just talk into the `ai-X` channels that you make, and it should respond. It only has about 5 messages of memory, and you can clear it's memory by typing $clear into the chat.

## Limitations

* Only 5 messages of memory
* It sees all chat members as the same person
* It will respond to every single message
