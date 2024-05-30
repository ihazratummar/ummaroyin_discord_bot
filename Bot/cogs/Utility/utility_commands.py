import discord
from discord.ext import commands
from config import Bot
from discord import app_commands
import datetime, time
import asyncio


class Utility(commands.Cog):
    def __init__(self, bot : Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description= "Get all the commands list")
    async def help(self, interaction: commands.Context):
        embed = discord.Embed(
            title= "Help",
            description= "List of commands all the commands",
            color= 0x00FFFF
        )

        for c in self.bot.cogs:
             cog = self.bot.get_cog(c)
             if any(cog.walk_commands()):
                 embed.add_field(name=cog.qualified_name, value= " , ".join(f"`{i.name}`" for i in cog.walk_commands()), inline= False)
        await interaction.send(embed=embed)


    @commands.hybrid_command(name="ping", description="server ping")
    async def ping(self, interaction: commands.Context):
        await interaction.send(
            f"Ping {round(self.bot.latency * 1000)} ms"
        )

    @commands.hybrid_command(name="invite", description="Invite Link")
    async def invite(self, interaction: commands.Context):
        link = await interaction.channel.create_invite(max_age=0)
        await interaction.send(link)

    @commands.hybrid_command(name='server', description = "Get the server information")
    async def server_Info(self, ctx: commands.Context):
        embed=discord.Embed(title=f"{ctx.guild.name}", description="Information of this Server", color=0x00FFFF)
        embed.add_field(name="👑Owner", value=f"{ctx.guild.owner}", inline=True)
        embed.add_field(name="👥Total members", value=f"{ctx.guild.member_count}", inline=True)
        embed.add_field(name="🧸Categories", value=f"{len(ctx.guild.categories)}", inline=True)
        embed.add_field(name="🔮Total Text Channels", value=f"{len(ctx.guild.text_channels)}", inline=True)
        embed.add_field(name="🎑Total Voice Channels", value=f"{len(ctx.guild.voice_channels)}", inline=True)
        embed.add_field(name="🎐Total Roles", value=f"{len(ctx.guild.roles)}", inline=True)
        embed.set_thumbnail(url= ctx.guild.icon._url)
        embed.set_footer(text= f"ID: {ctx.guild.id} | Server Created - {ctx.guild.created_at}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="userinfo", description= "Display a user's info")
    async def userinfo(self, ctx: commands.Context, * , user: discord.Member = None):
        if user is None:
            user = ctx.author

            # Format the datetime objects
        account_created = user.created_at.strftime("%A, %d %B %Y %H:%M")
        server_joining_date = user.joined_at.strftime("%A, %d %B %Y %H:%M")
        embed=discord.Embed(title=f"{user.name}", description="", color=0x00FFFF)
        embed.add_field(name="ID", value=f"{user.id}", inline=True)
        embed.add_field(name="Nickname", value=f"{user.nick}", inline=True)
        embed.add_field(name="", value=f"", inline=True)
        embed.add_field(name="Account Created", value= f"> `{account_created}`" ,inline= False)
        embed.add_field(name="Server joining Date", value=f"> `{server_joining_date}`", inline=False)

        if len(user.roles) >1:
            role_string = '  '.join([r.mention for r in user.roles][1:])
            embed.add_field(name= "Roles[{}]".format(len(user.roles)-1), value=f"{role_string}", inline= False)
        embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar._url}")
        embed.set_thumbnail(url=f"{user.avatar._url}")

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description = "Display a User's Avatar")
    async def avatar(self, ctx: commands.Context, user:discord.Member = None):
        if user is None:
            user = ctx.author
        
        embed=discord.Embed(title=f"{user.name}", description=f"[Avatar URL]({user.avatar.url})", color=0x00FFFF)
        embed.set_image(url=f"{user.avatar._url}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name= "channelinfo")
    async def channelinfo(self, ctx: commands.Context, * ,channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        embed=discord.Embed(title=f"Channel Info: {channel.name}",color=0x00FFFF)
        embed.add_field(name=f"Channel Name", value=f"<#{channel.id}>", inline=False)
        embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No Topic Set'}", inline= False),
        embed.add_field(name="Channel Category", value=f"{channel.category.name if channel.category else 'No categoty'}", inline= False)
        embed.add_field(name="Position", value=f"{channel.position}", inline=True)
        embed.add_field(name='NSFW', value=f"{channel.is_nsfw()}", inline=True),
        embed.add_field(name="NEWS", value=f"{channel.is_news()}", inline= True)
        embed.set_footer(text=f"ID: {channel.id} | Created At : {channel.created_at.strftime('%A, %d %B %Y %H:%M')}"),
        embed.set_thumbnail(url=f"{ctx.guild.icon._url}")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
        