import inspect
import os
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from humanize import precisedelta

from bot import __version__
from core import embeds
from core.colours import Colours
from core.guild_ids import guild_ids


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="about", description="Some info about this bot!", guild_ids=guild_ids)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx: SlashContext):
        embed = discord.Embed(
            description="...is a currency bot with :third_place: as its currency! To start earning medals, type `/compete`. You can look at all the commands by typing `/` then scrolling through my commands!",
            colour=Colours.BRONZE)
        embed.set_author(name="Bronze Medalist", url="https://bronzemedalist.netlify.app")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Version", value="v" + __version__)
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)))
        embed.add_field(name="Medals", value="{:,}".format(self.bot.medals))
        embed.add_field(name="Latency", value="{:.3f}ms".format(self.bot.latency * 1000))
        embed.add_field(name="Uptime", value=precisedelta(datetime.now() - self.bot.startup))
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Invite link", value=f"[Click me]({self.bot.invite} \"{self.bot.invite}\")")
        embed.add_field(name="GitHub",
                        value="[Click me](https://github.com/realcyguy/bronze-medalist \"realcyguy/bronze-medalist\")")
        embed.add_field(name="Website",
                        value=f"[Click me](https://bronzemedalist.netlify.app \"bronzemedalist.netlify.app\")")
        embed.set_footer(text="Made by RealCyGuy#0873!")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Get the invite link of this bot.", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def invite(self, ctx: SlashContext):
        embed = discord.Embed(description=f"You can invite me to your server with my [invite link]({self.bot.invite})!",
                              colour=Colours.BRONZE)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="source", description="Get the source code.",
                       options=[create_option(name="command", description="The command you want to get the source of.",
                                              option_type=3, required=False)], guild_ids=guild_ids)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def source(self, ctx: SlashContext, command: str = None):
        source_url = "https://github.com/RealCyGuy/Bronze-Medalist"
        if command is None:
            embed = discord.Embed(title="Bronze Medalist's Source Code",
                                  description=source_url + "\n\n" + "To get source for a specific command, use "
                                                                    "`/source {command}`", colour=Colours.BRONZE)
            await ctx.send(embed=embed)
            return

        not_found = embeds.error("Command not found!")
        obj = self.bot.get_command(command)
        if obj is None:
            return await ctx.send(embed=not_found)

        src = obj.callback.__code__
        lines, file_start = inspect.getsourcelines(src)
        sourcecode = inspect.getsource(src).replace("```", "")
        branch = "master"
        if obj.callback.__module__.startswith("discord"):
            location = obj.callback.__module__.replace(".", "/") + ".py"
            source_url = "https://github.com/Rapptz/discord.py"
        elif obj.callback.__module__.startswith("jishaku"):
            location = obj.callback.__module__.replace(".", "/") + ".py"
            source_url = "https://github.com/Gorialis/jishaku"
        else:
            location = os.path.relpath(src.co_filename).replace("\\", "/")
            branch = "prod"

        if obj.callback.__module__.startswith("cogs.events") or obj.callback.__module__.startswith("jishaku"):
            prefix = self.bot.command_prefix
        else:
            prefix = "/"
        embed = discord.Embed(
            title=f"Source code of {prefix}{command}.",
            colour=Colours.BRONZE)

        sourcecode = sourcecode.splitlines(True)
        for index, line in enumerate(sourcecode):
            if line.startswith(" " * 4):
                sourcecode[index] = line[4:]
        sourcecode = "".join(sourcecode)

        file_end = file_start + len(lines) - 1
        if len(sourcecode) > 1900:
            embed.description = "{}/blob/{}/{}#L{}-L{}".format(source_url, branch, location, file_start, file_end)
        else:
            embed.description = "<{}/blob/{}/{}#L{}-L{}>\n```py\n{}```".format(source_url, branch, location, file_start,
                                                                               file_end, sourcecode)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ping", description="Get the latency of the bot.", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx: SlashContext):
        embed = discord.Embed(title="Pong!", description="{:.5f}ms".format(self.bot.latency * 1000),
                              colour=Colours.BRONZE)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
