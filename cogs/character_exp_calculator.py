import discord

from discord.ext import commands

class CharacterExpCalculator(commands.cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=["char_exp"])
	async def character_exp_calculator(self, ctx):
		pass

def setup(client):
	client.add_cog(CharacterExpCalculator(client))