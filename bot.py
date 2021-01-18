import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix="./", activity=discord.Game(name="./help"), help_command=None)

def default_embed_template():
    embedded_message = discord.Embed(title="Unital Bot", colour=discord.Colour.teal())
    embedded_message.set_footer(text="Written by richie#2785", icon_url="https://cdn.discordapp.com/avatars/139204017296375808/9d560b7112b6f3233d323322feb7ca5d.png?size=128")
    return embedded_message

@client.event
async def on_ready():
    print(f"{client.user} has connected to {len(client.guilds)} server(s)")
    
@client.event
async def on_disconnect():
    print(f"{client.user} has disconnected")

@client.event
async def on_resumed():
    print(f"{client.user} has reconnected")

@client.event
async def on_command_error(ctx, error):
    await ctx.send(content=f"Error: Invalid command")

@client.command()
async def help(ctx):
    embedded_message = default_embed_template()

    args = ctx.message.content.split()

    if len(args) == 1:
        embedded_message.add_field(name="Bot Commands", value="`./help <command>`")
        await ctx.send(embed=embedded_message) 

@client.command()
async def ping(ctx):
    args = ctx.message.content.split()

    if len(args) > 1:
        await ctx.send(content=f"Usage: ./ping")
    else:
        await ctx.send(content=f"{round(client.latency*1000)}ms")

client.run(os.getenv('TOKEN'))