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

## Run

```bash
python ./gptbot/bot.py
```

## Configure in discord

You'll need a text channel starting with `ai-`

The channel needs to have a description with a JSON value like:

```json
TODO: write up
```
