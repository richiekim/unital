import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from help_text import HelpText
from common_functions import default_embed_template

load_dotenv()
client = commands.Bot(command_prefix="!", help_command=None)
client.activity = discord.Game(name=f"{client.command_prefix}help")

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

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been loaded.")

@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    print("Starting to unload")
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been unloaded.")

@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    await ctx.send(content=f"{extension} has been reloaded.")

@client.command(hidden=True)
async def help(ctx):
    args = ctx.message.content.split()

    helptxt = HelpText()

    embedded_message = default_embed_template(ctx, f"{client.user.name}")
    if len(args) == 1:
        cmd_msg = ""
        for cmd in client.commands:
            if not cmd.hidden:
                cmd_msg += f"\n{helptxt.usage[cmd.name]}\n"
                cmd_msg += f"{helptxt.description[cmd.name]} Use `{client.command_prefix}help {cmd.name}` for more details.\n"
        embedded_message.add_field(name="Commands", value=cmd_msg)
        await ctx.send(embed=embedded_message) 
    elif len(args) == 2:
        found = False
        for cmd in client.commands:
            if cmd.name == args[1]:
                found = True
                break

        if found:
            cmd_msg = f"{helptxt.description[cmd.name]}\n\n"
            cmd_msg += f"Usage: {helptxt.usage[cmd.name]}\n\n"
            cmd_msg += f"{helptxt.details[cmd.name]}\n"
            embedded_message.add_field(name=f"{client.command_prefix}{cmd.name} command details", value=cmd_msg)
            await ctx.send(embed=embedded_message) 
        else:
            raise commands.ArgumentParsingError(message=f"Command '{args[1]}' does not exist. Cannot provide help.")
    else:
        await ctx.send(f"Usage: {client.command_prefix}help")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(os.getenv("TOKEN"))