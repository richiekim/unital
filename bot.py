import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix="!")
client.activity = discord.Game(name=f"{client.command_prefix}help")

def default_embed_template():
    embedded_message = discord.Embed(title="Unital Bot", colour=discord.Colour.teal())
    embedded_message.set_footer(text="Written by richie#2785", icon_url=os.getenv("ICON"))
    return embedded_message

@client.event
async def on_ready():
    print(f"{client.user} has connected to {len(client.guilds)} server(s).")
    
@client.event
async def on_disconnect():
    print(f"{client.user} has disconnected.")

@client.event
async def on_resumed():
    print(f"{client.user} has reconnected.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(content=f"Error: Command not found.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(content=f"Error: Command denied. Only the bot's owner can use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=f"Error: Missing required arguments. Check out the {client.command_prefix}help command for usage.")
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send(content=f"Error: {error}")
    elif isinstance(error, commands.ExtensionError):
        await ctx.send(content=f"Error: {error}. Please contact the bot's owner.")
    else:
        print(f"Uncaught Exception: {error}")
        await ctx.send(content=f"Uncaught Exception: {error}. Please contact the bot's owner.")

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been loaded.")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    print("Starting to unload")
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been unloaded.")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been reloaded.")

# @client.command()
# async def help(ctx):
#     embedded_message = default_embed_template()

#     args = ctx.message.content.split()

#     if len(args) == 1:
#         embedded_message.add_field(name="Bot Commands", value="`!help <command>`")
#         await ctx.send(embed=embedded_message) 

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.getenv("TOKEN"))