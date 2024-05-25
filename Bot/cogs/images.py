import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import requests
import asyncpraw
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()



class Images(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="imgur", description="search for images")
    async def imgur(self, interaction: discord.Interaction, *, query: str):
        headers = {"Authorization": "Client-ID 20c2904655c6a1f"}
        params = {"q": query}
        response = requests.get(
            "https://api.imgur.com/3/gallery/search/", headers=headers, params=params
        )

        if response.status_code == 200:
            data = json.loads(response.content.decode("utf-8"))
            images = [
                item for item in data["data"] if "images" in item and item["images"]
            ]

            if images:
                random_image = random.choice(images)
                image_url = random.choice(random_image["images"])["link"]

                embed = discord.Embed(
                    title=f'Results for **{query}**', color=discord.Color.blue()
                )
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    f'Sorry, no images found for "{query}"'
                )
        else:
            await interaction.response.send_message(
                "Sorry, there was an error processing your request. Please try again later."
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
