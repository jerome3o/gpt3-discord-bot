import discord


def get_context_id_from_message(message: discord.Message):
    channel: discord.TextChannel = message.channel
    channel_name = channel.name
    guild_name = message.guild.name
    guild_id = message.guild.id

    return f"{channel_name}_{guild_name}_{guild_id}"

    # TODO: get identifier for discord server
    # server_name = channel.
