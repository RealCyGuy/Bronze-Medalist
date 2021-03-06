import asyncio
import random
from math import floor

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from core import embeds
from core.colours import Colours
from core.guild_ids import guild_ids


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="compete", description="Compete to earn some bronze medals.", guild_ids=guild_ids)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def compete(self, ctx: SlashContext):
        embed = discord.Embed(title="Searching for competitions...", description="\u2591" * 10 + " [0.0%]",
                              colour=Colours.BRONZE)
        msg = await ctx.send(embed=embed)

        async def load():
            bar = 0
            while bar < 10:
                await asyncio.sleep(0.4)
                bar += random.uniform(1, 4)
                if bar >= 9.5:
                    bar = 10.0
                    embed.title = "Waiting for results..."
                elif bar > 6:
                    embed.title = "Competing..."
                elif bar > 3:
                    embed.title = "Entering competitions..."
                embed.description = ("\u2588" * round(bar)) + (
                        "\u2591" * round(10 - bar) + " [" + str(round(bar * 10, 1)) + "%]")
                await msg.edit(embed=embed)

        async def update_medals():
            # Relative weights: 10, 7, 9, 9, 13, 14, 13, 9, 8, 6, 2
            medals_earned = random.choices([None, 6, 7, 8, 14, 15, 16, 17, 19, 20, random.randint(60, 80)],
                                           cum_weights=(10, 17, 26, 35, 48, 62, 75, 84, 92, 98, 100))[0]
            if medals_earned:
                user = self.bot.db().get(str(ctx.author_id))
                medals = medals_earned
                if user:
                    medals = medals_earned + user["medals"]
                    self.bot.db().update({"medals": medals}, str(ctx.author_id))
                else:
                    self.bot.db().insert({"medals": medals_earned}, key=str(ctx.author_id))
                nonlocal result
                result = ("WOOOOOOW!" if medals_earned > 59 else "Wow!") + " You won " + str(
                    medals_earned) + " :third_place:! You now have " + "{:,}".format(medals) + " :third_place:."

        result = "You won zero :third_place:. Better luck next time!"
        await asyncio.gather(load(), update_medals(), return_exceptions=True)
        embed.title = result
        await msg.edit(embed=embed)

    @cog_ext.cog_slash(name="dig", description="Dig up some medals.", guild_ids=guild_ids)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def dig(self, ctx: SlashContext):
        medals_earned = random.randrange(20, 30)
        user = self.bot.db().get(str(ctx.author_id))
        if user:
            medals = medals_earned + user["medals"]
            self.bot.db().update({"medals": medals}, str(ctx.author_id))
        else:
            medals = medals_earned
            self.bot.db().insert({"medals": medals_earned}, key=str(ctx.author_id))

        place = random.choice(
            ["the ground", "a place", "a whiteboard", "china", "sample text", "your room", "a swimming pool",
             "my pocket", "the library's comic section", "the alley between two competing fast food chains",
             "the pineapple basket", "the bank", "a grass molecule", "air", "that ice cream place", "a napkin factory",
             "your medals", "water"])
        embed = discord.Embed(title=f"You dug {medals_earned} :third_place: up in {place}.",
                              description="You now have {:,}:third_place:.".format(medals), colour=Colours.BRONZE)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="interest", description="Gain 2% of your current medals.", guild_ids=guild_ids)
    @commands.cooldown(1, 76, commands.BucketType.user)
    async def interest(self, ctx: SlashContext):
        user = self.bot.db().get(str(ctx.author_id))
        medals = 0
        medals_earned = 0
        total_medals = 0
        if user:
            medals = user["medals"]
            medals_earned = floor(medals * 0.02)
            total_medals = medals + medals_earned
            self.bot.db().update({"medals": total_medals}, str(ctx.author_id))
        embed = discord.Embed(title="Your seventy-six second-ly interest report.", colour=Colours.BRONZE)
        if medals_earned:
            embed.description = f"With 2% interest, you earned {medals_earned} :third_place: and now have {total_medals} :third_place:."
        else:
            embed.description = f"Your {medals} :third_place: aren't enough to get you any interest, try `/compete`."
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="balance", description="See how many bronze medals you or another user has.",
                       options=[create_option(name="user", description="The user you want to see the balance of.",
                                              option_type=6, required=False)], guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx: SlashContext, user: discord.User = None):
        user = user if user else ctx.author
        user_db = self.bot.db().get(str(user.id))
        if user_db:
            medals = user_db["medals"]
        else:
            medals = 0
        embed = discord.Embed(title=user.name + "#" + user.discriminator + "'s balance",
                              description="**" + "{:,}".format(medals) + "** :third_place:", colour=Colours.BRONZE)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="give", description="Give some medals to another user!",
                       options=[create_option(name="user", description="The user you want to give medals to.",
                                              option_type=6, required=True),
                                create_option(name="amount", description="The amount of medals to give.", option_type=4,
                                              required=True)],
                       guild_ids=guild_ids)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def give(self, ctx: SlashContext, user: discord.User, amount: int):
        if user == ctx.author:
            return await ctx.send(embed=embeds.error("You can't send medals to yourself."))
        # if user.bot:
        #     return await ctx.send(embed=embeds.error("You can't send medals to bots."))
        if amount < 1:
            return await ctx.send(embed=embeds.error("You have to give at least one medal."))
        user_db = self.bot.db().get(str(ctx.author_id))
        medals = 0
        if user_db:
            medals = user_db["medals"]
        if medals < amount:
            return await ctx.send(embed=embeds.error("You don't have enough medals to give."))
        self.bot.db().update({"medals": medals - amount}, str(ctx.author_id))
        # medals_receiving = ceil(amount * 0.9)
        medals_receiving = amount
        receiver_db = self.bot.db().get(str(user.id))
        receiver_medals = 0
        if receiver_db:
            receiver_medals = receiver_db["medals"]
            self.bot.db().update({"medals": receiver_medals + medals_receiving}, str(user.id))
        else:
            self.bot.db().insert({"medals": medals_receiving}, str(user.id))
        embed = discord.Embed(
            title=f"Gave {str(medals_receiving)} :third_place: to {user.name}#{user.discriminator}.",
            description="You now have " +
                        str(medals - amount) + " :third_place: and they have " + str(
                receiver_medals + medals_receiving) + " :third_place:.", colour=Colours.BRONZE)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="fortysixpercentchancetodouble",
                       description="A forty-six chance to double the medals you gamble!",
                       options=[
                           create_option(name="amount", description="The amount of medals to gamble.", option_type=4,
                                         required=True)],
                       guild_ids=guild_ids)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def fortysixpercentchancetodouble(self, ctx: SlashContext, amount: int):
        if amount < 1:
            return await ctx.send(embed=embeds.error("You have to gamble at least one medal."))
        user = self.bot.db().get(str(ctx.author_id))
        medals = 0
        if user:
            medals = user["medals"]
        if amount > medals:
            return await ctx.send(embed=embeds.error("You don't have enough medals to gamble!"))
        embed = discord.Embed(colour=Colours.BRONZE)
        if random.random() < 0.46:
            updated_medals = medals + amount
            embed.title = f"You won {amount} :third_place:!"
        else:
            updated_medals = medals - amount
            embed.title = f"Oof, you lost {amount} :third_place:."
        self.bot.db().update({"medals": updated_medals}, str(ctx.author_id))
        embed.description = f"You now have {updated_medals} :third_place:."
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Currency(bot))
