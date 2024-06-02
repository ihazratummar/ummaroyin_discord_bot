import discord
from discord.ext import commands, tasks
from config import Bot
from dotenv import load_dotenv
import os
import requests
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

DEV_API_KEY = os.getenv("DEV_API_KEY")
FOLLOWERS_FILE = "data/followers.json"

class Notification(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.previous_followers = self.load_followers()
        self.check_new_followers.start()

    def fetch_followers(self):
        url = "https://dev.to/api/followers/users"
        response = requests.get(url, headers={'api-key': DEV_API_KEY})
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to fetch followers: {response.status_code}")
            return []

    def load_followers(self):
        if os.path.exists(FOLLOWERS_FILE):
            with open(FOLLOWERS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_followers(self, followers):
        with open(FOLLOWERS_FILE, 'w') as f:
            json.dump(followers, f)

    @tasks.loop(seconds=10)
    async def check_new_followers(self):
        current_followers = self.fetch_followers()
        if not current_followers:
            return

        # Find new followers by comparing with previous followers
        new_followers = [follower for follower in current_followers if follower not in self.previous_followers]
        channel = os.getenv("DEV_NOTIFICATION_CHANNEL")
        if new_followers:
            channel = self.bot.get_channel(channel)
            if channel:
                for follower in new_followers:
                    embed = discord.Embed(title="New Follower!", description=None, color=0x00FFFF)
                    embed.add_field(name="Name", value=follower['name'], inline=False)
                    embed.add_field(name="Username", value=follower['username'], inline=False)
                    embed.set_thumbnail(url=follower['profile_image'])
                    embed.set_footer(text=follower['created_at'])
                    await channel.send(embed=embed)
            else:
                logging.error("Channel not found!")

            # Update the previous followers list and save it
            self.previous_followers.extend(new_followers)
            self.save_followers(self.previous_followers)

    @check_new_followers.before_loop
    async def before_check_new_followers(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(Notification(bot))
