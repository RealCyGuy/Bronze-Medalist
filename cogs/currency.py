import asyncio
import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from core.colours import Colours
from core.guild_ids import guild_ids


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.compete_cooldown = {}

    @cog_ext.cog_slash(name="compete", description="Compete to earn some bronze medals.", guild_ids=guild_ids)
    async def compete(self, ctx: SlashContext):
        await ctx.respond(eat=True)
        cooldown = self.compete_cooldown.get(str(ctx.author_id), None)
        now = datetime.now()
        if cooldown:
            difference = now - cooldown
            if difference < timedelta(seconds=20):
                embed = discord.Embed(title="You are entering competitions too fast!",
                                      description="Try again in " + str(
                                          round((timedelta(seconds=20) - difference).total_seconds())) + " seconds.",
                                      color=Colours.BRONZE)
                return await ctx.send(ctx.author.mention, embed=embed)
        self.compete_cooldown[str(ctx.author_id)] = now
        embed = discord.Embed(title="Searching for competitions...", description="\u2591" * 10 + " [0.0%]",
                              colour=Colours.BRONZE)
        msg = await ctx.send(ctx.author.mention, embed=embed)
        bar = 0
        while bar < 10:
            await asyncio.sleep(0.4)
            bar += random.uniform(1, 4)
            if bar >= 9.5:
                bar = 10.0
            elif bar > 6:
                embed.title = "Competing..."
            elif bar > 3:
                embed.title = "Entering competitions..."
            embed.description = ("\u2588" * round(bar)) + (
                    "\u2591" * round(10 - bar) + " [" + str(round(bar * 10, 1)) + "%]")
            await msg.edit(embed=embed)
        # Relative weights: 10, 7, 9, 9, 13, 14, 13, 9, 8, 6, 2
        medals_earned = random.choices([None, 6, 7, 8, 14, 15, 16, 17, 19, 20, random.randint(60, 80)],
                                       cum_weights=(10, 17, 26, 35, 48, 62, 75, 84, 92, 98, 100))[0]
        if medals_earned:
            user = self.bot.db.get(str(ctx.author_id))
            medals = medals_earned
            if user:
                medals = medals_earned + user["medals"]
                self.bot.db.update({"medals": medals}, str(ctx.author_id))
            else:
                self.bot.db.insert({"medals": medals_earned}, key=str(ctx.author_id))
            embed.title = ("WOOOOOOW!" if medals_earned > 59 else "Wow!") + " You won " + str(
                medals_earned) + " :third_place:! You now have " + "{:,}".format(medals) + " :third_place:."
        else:
            embed.title = "You won zero :third_place:. Better luck next time!"
        await msg.edit(embed=embed)

    @cog_ext.cog_slash(name="balance", description="See how many bronze medals you or another user has.",
                       options=[create_option(name="user", description="the user you want to see the balance of.",
                                              option_type=6, required=False)], guild_ids=guild_ids)
    async def balance(self, ctx: SlashContext, user: discord.User = None):
        await ctx.respond(eat=True)
        user = user if user else ctx.author
        user_db = self.bot.db.get(str(user.id))
        if user_db:
            medals = user_db["medals"]
        else:
            medals = 0
        embed = discord.Embed(title=user.name + "#" + user.discriminator + "'s balance",
                              description="**" + "{:,}".format(medals) + "** :third_place:", colour=Colours.BRONZE)
        await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Currency(bot))
