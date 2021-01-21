import discord

from discord.ext import commands

MYSTIC = 10000
FINE = 2000
NORMAL = 400

class WeaponExpCalculator(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=["weapon_exp"])
	async def calculate_weapon_exp(self, ctx, curr_level, goal_level, curr_exp, mystic_ore_count, fine_ore_count, ore_count):
		args = ctx.message.content.split()

		if len(args) == 7:
			await ctx.send("Correct number of args")
		else:
			await ctx.send("Usage: !")

		await ctx.send(len(args))
		await ctx.send(args)

def setup(client):
	client.add_cog(WeaponExpCalculator(client))