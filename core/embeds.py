import discord
from core.colours import Colours


def error(message: str):
    return discord.Embed(colour=Colours.RED, title=message)
