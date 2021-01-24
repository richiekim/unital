import discord 

from discord.ext import commands

class Ping(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def ping(self, ctx):
		args = ctx.message.content.split()

		if len(args) > 1:
			await ctx.send(content=f"Usage: {self.client.command_prefix}ping")
		else:
			await ctx.send(content=f"{round(self.client.latency*1000)}ms")

def setup(client):
	client.add_cog(Ping(client))