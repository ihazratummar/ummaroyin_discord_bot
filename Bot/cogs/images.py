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

    @app_commands.command(name= "images_search", description="search a images")
    async def image_search(self, interaction : discord.Interaction, q:str):
        key = os.getenv("pixabay_API")
        response = requests.get(f"https://pixabay.com/api/?key={key}&q={q}")

        data = response.json()

        images = [item for item in data["hits"] if "previewURL" in item]
        if not images:
            await interaction.response.send_message("No Images Found.")
            return
        # preview_url = [item["previewURL"] for item in images]

        random_images = random.choice(images)

        embed = discord.Embed(
            title=f"Your search result for {q}",
            description= "",
            color= discord.Color.dark_embed()
        )
        embed.add_field(name="Likes", value=random_images["likes"])
        embed.add_field(name="Downloads", value=random_images["downloads"])
        embed.add_field(name="Views", value=random_images["views"])
        embed.set_image(url= random_images["largeImageURL"])
        embed.set_author(name=random_images["user"], icon_url=random_images["userImageURL"])

        button1 = discord.ui.Button(
            label="Open Image", 
            url=random_images["pageURL"],
            style= discord.ButtonStyle.link
        )
        view = discord.ui.View()
        view.add_item(button1)

        await interaction.response.send_message(embed= embed, view= view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
