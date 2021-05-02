__version__ = "0.2.10"

import os
from datetime import datetime

import discord
from deta import Deta
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from dotenv import load_dotenv

from core.colours import Colours

load_dotenv()


class BronzeMedalist(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=os.environ.get("PREFIX", "b."),
                         activity=discord.Game("bronze medals op | /about | v" + __version__),
                         intents=discord.Intents.all(), *args, **kwargs)
        self.remove_command("help")
        self.loading_cogs = ["cogs.currency", "cogs.events", "cogs.misc", "jishaku"]
        self.event_starters = list(
            map(int, str(os.environ.get("EVENT_STARTER_IDS", None)).split(","))) if os.environ.get(
            "EVENT_STARTER_IDS", None) else None
        # Get deta key from .env
        self.deta_key = os.environ.get("DETA_KEY", None)
        if self.deta_key is None or len(self.deta_key.strip()) == 0:
            print("\nA Deta Project Key is necessary for the bot to function.\n")
            raise RuntimeError
        # Data for the last message event
        self.last_event = {"in_progress": False, "users": [], "channel": 0}
        # Startup time
        self.startup = datetime.now()
        # Startup total medals
        self.medals = 0
        # Startup message
        print('=' * 24)
        print("Bronze Medalist")
        print("By: Cyrus")
        print('=' * 24)

    async def on_ready(self):
        print('-' * 24)
        print('Logged in as:')
        print(self.user.name + "#" + self.user.discriminator)
        print("Id: " + str(self.user.id))
        print(f"Discord version: {discord.__version__}")
        print(f"Bot version: {__version__}")
        print('-' * 24)
        print("I am logged in and ready!")
        # Invite link
        self.invite = "https://discord.com/api/oauth2/authorize?client_id=" + str(
            self.user.id) + "&permissions=2048&scope=applications.commands%20bot"
        self.invite = os.environ.get("INVITE", self.invite)
        # Start total medals loop
        self.update_medals.start()

    def db(self):
        deta = Deta(self.deta_key)
        return deta.Base(os.environ.get("DETABASE_NAME", "BronzeMedalist"))

    def load_cogs(self):
        for cog in self.loading_cogs:
            print(f"Loading {cog}...")
            try:
                self.load_extension(cog)
                print(f"Successfully loaded {cog}.")
            except Exception as e:
                print(f"Failed to load {cog}. Error: {e}")

    async def on_message(self, message):
        if message.channel.id == self.last_event["channel"] and not message.author.bot:
            if message.author.id in self.last_event["users"]:
                await message.delete()
            else:
                self.last_event["users"].append(message.author.id)
        await self.process_commands(message)

    async def on_slash_command_error(self, context, exception):
        if isinstance(exception, commands.CommandOnCooldown):
            embed = discord.Embed(title="You are going too fast!",
                                  description=f"Try again in {exception.retry_after:.2f} seconds.", colour=Colours.RED)
            await context.send(embed=embed)
        else:
            raise exception

    @tasks.loop(minutes=3)
    async def update_medals(self):
        query = [{"medals?gt": 0}]
        medals = 0
        for page in self.db().fetch(query=query):
            for user in page:
                medals += user["medals"]
        self.medals = medals


bot = BronzeMedalist()
slash = SlashCommand(bot, sync_commands=True)
bot.load_cogs()

token = os.environ.get("TOKEN", None)
if token is None or len(token.strip()) == 0:
    print("\nA bot token is necessary for the bot to function.\n")
    raise RuntimeError
bot.run(token)
