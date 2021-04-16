import os

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from core.colours import Colours
from core.guild_ids import guild_ids


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="invite", description="Get the invite link of this bot.", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def invite(self, ctx: SlashContext):
        invite = "https://discord.com/api/oauth2/authorize?client_id=" + str(
            self.bot.user.id) + "&permissions=2048&scope=applications.commands%20bot"
        invite = os.environ.get("INVITE", invite)
        embed = discord.Embed(description=f"You can invite me to your server with my [invite link]({invite})!",
                              colour=Colours.BRONZE)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
