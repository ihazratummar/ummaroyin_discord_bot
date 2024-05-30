import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import requests
import asyncpraw
import random


class Fun(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="meme", description="get a random meme")
    async def meme(self, interaction: discord.Interaction):
        try:
            subreddits = [
                "memes",
                "dankmemes",
                "AdviceAnimals",
                "MemeEconomy",
                "terriblefacebookmemes",
            ]  # Add the desired subreddits here
            subreddit = subreddits[random.randint(0, len(subreddits) - 1)]
            response = requests.get(
                f"https://api.reddit.com/r/{subreddit}/random",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            data = response.json()
            meme_url = data[0]["data"]["children"][0]["data"]["url"]
            meme_title = data[0]["data"]["children"][0]["data"]["title"]
            meme_data = data[0]["data"]["children"][0]["data"]
            embed = discord.Embed(title=f"{meme_title}", color=0x00FFFF)
            embed.set_image(url=meme_url)
            embed.set_author(name=meme_data["author"])
            embed.set_footer(text=f"Reddit/{subreddit}")

            await interaction.response.send_message(
                embed=embed,
            )
        except Exception as e:
            print(f"Error retrieving meme: {e}")
            await interaction.response.send_message("sorry, i couldn't find")


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
