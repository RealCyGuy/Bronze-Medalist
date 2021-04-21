import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from core import embeds
from core.colours import Colours
from core.guild_ids import guild_ids


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="hi", description="Hi!", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hi(self, ctx: SlashContext):
        await ctx.send("Hi!")


def setup(bot):
    bot.add_cog(Fun(bot))
