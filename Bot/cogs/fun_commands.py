import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import requests
import asyncio
import random


class Fun(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="meme", description="get a random meme")
    async def meme(self, interaction: commands.Context):
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

            await interaction.send(
                embed=embed,
            )
        except Exception as e:
            print(f"Error retrieving meme: {e}")
            await interaction.send("sorry, i couldn't find")


    @commands.hybrid_command(name="joke", descriptio = "Tells a random joke.")
    async def joke(self, ctx: commands.Context):
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()
        setup = data["setup"]
        paunch_line = data["punchline"]

        await ctx.send(setup)
        await asyncio.sleep(3)
        await ctx.send(paunch_line)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
