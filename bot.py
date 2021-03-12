__version__ = "0.1.0"

import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from deta import Deta

from dotenv import load_dotenv

load_dotenv()


class BronzeMedalist(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="/", activity=discord.Game("bronze medals op"), *args, **kwargs)
        self.remove_command("help")
        self.loading_cogs = ["cogs.currency", "cogs.misc"]
        deta_key = os.environ.get("DETA_KEY", None)
        if deta_key is None or len(deta_key.strip()) == 0:
            print("\nA Deta Project Key is necessary for the bot to function.\n")
            raise RuntimeError
        deta = Deta(deta_key)
        self.db = deta.Base("BronzeMedalist")
        self.startup()

    async def on_ready(self):
        print('-' * 24)
        print('Logged in as:')
        print(bot.user.name + "#" + bot.user.discriminator)
        print("Id: " + str(bot.user.id))
        print(f"Discord version: {discord.__version__}")
        print(f"Bot version: {__version__}")
        print('-' * 24)
        print("I am logged in and ready!")

    def startup(self):
        print('=' * 24)
        print("Bronze Medalist")
        print("By: Cyrus")
        print('=' * 24)

    def load_cogs(self):
        for cog in self.loading_cogs:
            print(f"Loading {cog}...")
            try:
                self.load_extension(cog)
                print(f"Successfully loaded {cog}.")
            except Exception as e:
                print(f"Failed to load {cog}. Error type: {type(e).__name__}")


bot = BronzeMedalist()
slash = SlashCommand(bot, override_type=True, sync_commands=True)
bot.load_cogs()


token = os.environ.get("TOKEN", None)
if token is None or len(token.strip()) == 0:
    print("\nA bot token is necessary for the bot to function.\n")
    raise RuntimeError
else:
    bot.run(token)
