import discord
from discord.ext import commands
from discord import app_commands
from config import Bot
import requests
import asyncio
import random
from dotenv import load_dotenv
import os


load_dotenv()


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


    @commands.hybrid_command(name="gif", description = "Get a random gif")
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def gif(self, ctx:commands.Context, tag: str):
        api_key = os.getenv("GIPHY_API")
        url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&rating=g&tag={tag}"
        response = requests.get(url)
        
        if response.status_code != 200:
            await ctx.send("Connection Failed")
        data = response.json()
        if not data:
            await ctx.send("Gif data not found")

        embed_url = data["data"]["embed_url"]
        await ctx.send(embed_url)


    @commands.hybrid_command(name="pokemon", description ="Get a random pokemon name and image")
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def pokemon(self, ctx:commands.Context):
        response = requests.get("https://pokeapi.co/api/v2/pokemon-species/")
        total_pokemon = response.json()['count']

        random_id = random.randint(1, total_pokemon-1)

        pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_id}/")
        pokemon_data = pokemon_response.json()

        pokemon_name = pokemon_data['name']
        pokemon_image = pokemon_data['sprites']['other']['home']['front_default']
        pokemon_thumbnail = pokemon_data['sprites']['front_default']
        species = pokemon_data['species']['name']
        
        type = pokemon_data['types']
        type_names = [type_info['type']['name'] for type_info in type]
        type_text = ', '.join(type_name.capitalize() for type_name in type_names)

        embed=discord.Embed(title=f"{pokemon_name}", description=None, color=0x00FFFF)
        embed.set_thumbnail(url=f"{pokemon_thumbnail}")
        embed.add_field(name="Species", value=f"{species}", inline= True)
        embed.add_field(name="Type", value=f"{type_text}", inline= True)
        embed.set_image(url=f"{pokemon_image}")
        await ctx.send(embed=embed)


    @commands.hybrid_command(name="cat", description = "Get a random cat image with description")
    @commands.cooldown(4, 20, commands.BucketType.guild)
    async def cat(self, ctx: commands.Context, user: discord.Member = None):
        api_key = os.getenv("CAT_API_KEY")
        url = "https://api.thecatapi.com/v1/images/search?has_breeds=1"
        reponse = requests.get(url, headers={'x-api-key': f"{api_key}"})

        data = reponse.json()

        breed = [breed['breeds'] for breed in data]
        image = [image['url'] for image in data]
        cat = breed[0][0]
        cat_name = cat['name']
        cat_description = cat['description']
        cat_temperament = cat['temperament']

        embed=discord.Embed(title=f"{cat_name}", description=f">>> {cat_description}", color=0x00FFFF)
        embed.add_field(name="Temperament", value=f">>> {cat_temperament}", inline=False)
        embed.set_image(url=f"{image[0]}")

        if user:
            await ctx.send(user.mention,embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="dog", description = "Get a random cat image with description")
    @commands.cooldown(4, 20, commands.BucketType.guild)
    async def dog(self, ctx: commands.Context, user: discord.Member = None):
        api_key = os.getenv("DOG_API_KEY")
        url = "https://api.thedogapi.com/v1/images/search?has_breeds=1"
        reponse = requests.get(url, headers={'x-api-key': f"{api_key}"})

        data = reponse.json()

        breed = [breed['breeds'] for breed in data]
        image = [image['url'] for image in data]
        dog = breed[0][0]
        dog_name = dog['name']
        dog_temperament = dog['temperament'] 

        embed=discord.Embed(title=f"{dog_name}", description= None ,color=0x00FFFF)
        embed.add_field(name="Temperament", value=f">>> {dog_temperament}", inline=False)
        embed.set_image(url=f"{image[0]}")

        if user:
            await ctx.send(user.mention,embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="fact", description = "Get a random fact")
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def fact(self, ctx: commands.Context, user: discord.Member = None):
        api_key = os.getenv("API_NINJA")
        url = "https://api.api-ninjas.com/v1/facts"
        response = requests.get(url, headers={'X-Api-Key':f'{api_key}'})
        if response.status_code != 200:
            await ctx.send("Connection Failed")
        
        data =response.json()
        fact = [fact['fact'] for fact in data][0]
        embed=discord.Embed(title=f"Fact", description= None, color=0x00FFFF)
        embed.add_field(name=f">>> {fact}", value=" ", inline=False)
        
        if user:
            await ctx.send(user.mention,embed=embed)
        else:
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
