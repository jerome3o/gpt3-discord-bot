import discord


def get_context_id_from_message(message: discord.Message):
    channel: discord.TextChannel = message.channel
    channel_name = channel.name

    # TODO: get identifier for discord server
    # server_name = channel.
