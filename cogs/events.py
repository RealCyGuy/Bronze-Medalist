import asyncio
import http.client
import random

import discord
from discord.ext import commands

from core.checks import event_starter
from core.colours import Colours


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_winner(self, winner, medals):
        description = f"{winner.mention} won {medals} :third_place:."
        try:
            winner_db = self.bot.db().get(str(winner.id))
            if winner_db:
                self.bot.db().update({"medals": winner_db["medals"] + medals}, str(winner.id))
            else:
                self.bot.db().insert({"medals": medals}, str(winner.id))
        except http.client.RemoteDisconnected:
            description += " But an error occured."
        return description

    @commands.command("last")
    async def last(self, ctx: commands.Context, medals: int = 1000):
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
        event_time = random.randint(8, 12)
        await msg.edit(content=f"Event started! You can send messages for {event_time} seconds!")
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        while event_time > 0:
            await asyncio.sleep(1)
            event_time -= 1
            await msg.edit(content=f"Event started! You can send messages for {event_time} more seconds!")
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        winner = None
        while not winner and len(event["users"]) > 0:
            winner = ctx.guild.get_member(event["users"].pop())
        embed.title = "Last Message Event Results"
        if winner:
            embed.description = await self.update_winner(winner, medals)
        else:
            embed.description = "No one won."
        await ctx.send(embed=embed)
        await msg.edit(content="Event has ended.")
        event["in_progress"] = False
        event["users"] = []
        event["channel"] = 0

    @commands.command("react")
    @event_starter()
    async def react(self, ctx: commands.Context, medals: int = 1000):
        await ctx.message.delete()
        embed = discord.Embed(
            title="First Reaction Event!",
            description=f"In `First Reaction`, the first person who reacts to this message wins {medals} :third_place:. Hosted by {ctx.author.mention}!",
            colour=Colours.BRONZE)

        msg = await ctx.send("Event started.", embed=embed)
        await msg.add_reaction("\N{THIRD PLACE MEDAL}")

        def check(r, u):
            return msg.id == r.message.id and r.emoji == "\N{THIRD PLACE MEDAL}" and not u.bot

        embed.title = "Last Message Event Results"

        try:
            winner = (await self.bot.wait_for("reaction_add", check=check, timeout=120))[1]
        except asyncio.TimeoutError:
            embed.description = "No one won."
        else:
            embed.description = await self.update_winner(winner, medals)
        await ctx.send(embed=embed)
        await msg.edit(content="Event has ended.")


def setup(bot):
    bot.add_cog(Events(bot))
