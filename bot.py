__version__ = "0.2.0"

import os

import discord
from deta import Deta
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

load_dotenv()


class BronzeMedalist(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="b.", activity=discord.Game("bronze medals op"), intents=discord.Intents.all(), *args, **kwargs)
        self.remove_command("help")
        self.loading_cogs = ["cogs.currency", "cogs.misc"]
        self.db = self.init_deta_base()
        self.event_starters = list(
            map(int, str(os.environ.get("EVENT_STARTER_IDS", None)).split(","))) if os.environ.get(
            "EVENT_STARTER_IDS", None) else None
        # Last message event data
        self.last_event = {"in_progress": False, "users": [], "channel": 0}
        self.startup()

    async def on_ready(self):
        print('-' * 24)
        print('Logged in as:')
        print(self.user.name + "#" + self.user.discriminator)
        print("Id: " + str(self.user.id))
        print(f"Discord version: {discord.__version__}")
        print(f"Bot version: {__version__}")
        print('-' * 24)
        print("I am logged in and ready!")

    def init_deta_base(self):
        deta_key = os.environ.get("DETA_KEY", None)
        if deta_key is None or len(deta_key.strip()) == 0:
            print("\nA Deta Project Key is necessary for the bot to function.\n")
            raise RuntimeError
        deta = Deta(deta_key)
        return deta.Base(os.environ.get("DETABASE_NAME", "BronzeMedalist"))

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

    async def on_message(self, message):
        if message.channel.id == self.last_event["channel"] and not message.author.bot:
            if message.author.id in self.last_event["users"]:
                await message.delete()
            else:
                self.last_event["users"].append(message.author.id)
        await self.process_commands(message)


bot = BronzeMedalist()
slash = SlashCommand(bot, sync_commands=True)
bot.load_cogs()

token = os.environ.get("TOKEN", None)
if token is None or len(token.strip()) == 0:
    print("\nA bot token is necessary for the bot to function.\n")
    raise RuntimeError
else:
    bot.run(token)
