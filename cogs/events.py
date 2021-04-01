import asyncio
import http.client
import random

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from core.colours import Colours
from core.guild_ids import guild_ids
import core.embeds as embeds


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("last")
    async def last(self, ctx: commands.Context, medals: int = 1000):
        if ctx.author.id in self.bot.event_starters:
            await ctx.message.delete()
            event = self.bot.last_event
            if event["in_progress"]:
                return
            embed = discord.Embed(
                title="Last Message Event!",
                description=f"In `Last Message`, you only get to send one message. The last message gets the prize of {medals} :third_place:. Hosted by {ctx.author.mention}!",
                colour=Colours.BRONZE)
            msg = await ctx.send("Event starting in a few seconds.", embed=embed)
            event["channel"] = ctx.channel.id
            event["users"] = []
            await asyncio.sleep(3)
            event["in_progress"] = True
            event_time = random.randint(4, 7)
            await msg.edit(content=f"Event started! You can send messages for {event_time} seconds!")
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await asyncio.sleep(event_time)
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            winner = None
            while not winner and len(event["users"]) > 0:
                winner = ctx.guild.get_member(event["users"].pop())
            embed.title = "Last Message Event Results"
            if winner:
                embed.description = f"{winner.mention} won {medals} :third_place:."
                try:
                    winner_db = self.bot.db().get(str(winner.id))
                    if winner_db:
                        self.bot.db().update({"medals": winner_db["medals"] + medals}, str(winner.id))
                    else:
                        self.bot.db().insert({"medals": medals}, str(winner.id))
                except http.client.RemoteDisconnected:
                    embed.description += " But an error occured."
            else:
                embed.description = "No one won."
            await ctx.send(embed=embed)
            await msg.edit(content="Event has ended.")
            event["in_progress"] = False
            event["users"] = []
            event["channel"] = 0


def setup(bot):
    bot.add_cog(Events(bot))
