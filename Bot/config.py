#config.py
# region imports <- This is foldable
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord import Activity, ActivityType
import datetime, time

# endregion

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

exts = [
    "cogs.error",
    "cogs.general",
    "cogs.fun_commands",
    "cogs.media_commands",
    "cogs.games",
    "cogs.welcomer",
    # "cogs.Rewards.level",
    "cogs.Automod.automod",
    "cogs.Utility.utility_commands",
    "cogs.notification",
    "cogs.logs"
]


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def on_ready(self):
        for ext in exts:
            await self.load_extension(ext)
        print("loaded all cogs")


        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
        print("Bot is ready.")

        await self.change_presence(
            activity=discord.Game(name="Moderating CrazyForSurprise")
        )


if __name__ == "__main__":
    bot = Bot(command_prefix=".", intents=discord.Intents.all(), help_command = None)
    bot.run(token)