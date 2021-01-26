import discord
import json
import math

from discord.ext import commands
from common_functions import default_embed_template, use_exp_mat

MYSTIC = 10000
FINE = 2000
NORMAL = 400
ASCENSION_MILESTONES = [90, 80, 70, 60, 50, 40, 20]

class WeaponExpCalculator(commands.Cog):
	def __init__(self, client):
		self.client = client



	def add_exp(self, next_level_exp, curr_level, level_upto, curr_exp, mystic_count, fine_count, normal_count):
		fine_ore_refunded = 0
		normal_ore_refunded = 0
		wasted_exp = 0

		while curr_level < level_upto and mystic_count + fine_count + normal_count > 0:
			total_exp_next_level = int(next_level_exp[str(curr_level)])

			# Use materials until curr_level is over total_exp_next_level starting for those that give the most exp to the least
			curr_exp, mystic_count = use_exp_mat(curr_exp, total_exp_next_level, mystic_count, MYSTIC, True)
			curr_exp, fine_count = use_exp_mat(curr_exp, total_exp_next_level, fine_count, FINE, True)
			curr_exp, normal_count = use_exp_mat(curr_exp, total_exp_next_level, normal_count, NORMAL, True)

			# Calculate exp overflow
			while True:
				if curr_exp >= int(next_level_exp[str(curr_level)]):
					if curr_level + 1 in ASCENSION_MILESTONES:
						# Calculate refunded ores if any
						wasted_exp = curr_exp - int(next_level_exp[str(curr_level)])
						fine_ore_refunded = math.floor(wasted_exp/FINE)
						fine_count += fine_ore_refunded

						wasted_exp -= fine_ore_refunded*FINE
						normal_ore_refunded = math.floor(wasted_exp/NORMAL)
						normal_count += normal_ore_refunded

						wasted_exp -= normal_ore_refunded*NORMAL

						curr_exp = 0
						curr_level += 1

						return curr_level, curr_exp, mystic_count, fine_count, normal_count, fine_ore_refunded, normal_ore_refunded, wasted_exp
					else:
						curr_exp = curr_exp - int(next_level_exp[str(curr_level)])
						curr_level += 1
				else:
					break
		return curr_level, curr_exp, mystic_count, fine_count, normal_count, fine_ore_refunded, normal_ore_refunded, wasted_exp

	def calculate(self, embed_msg, rarity, curr_level, goal_level, curr_exp, mystic_count, fine_count, normal_count):
		with open(f"./wep_exp_per_level/wep_exp_per_level_{rarity}.json", "r") as f:
			next_level_exp = json.load(f)
		f.close()

		if not str(curr_level) in next_level_exp:
			raise commands.ArgumentParsingError(message="Please enter a valid weapon level.")

		if not str(goal_level) in next_level_exp:
			raise commands.ArgumentParsingError(message="Please enter a valid goal level.")

		if curr_exp > int(next_level_exp[str(curr_level)]):
			raise commands.ArgumentParsingError(message="Invalid current weapon experience points value.")

		embed_msg.add_field(name="**Before**", value=f"__Weapon__\nWeapon rarity: {rarity}:star:\nWeapon level: {curr_level}\nCurrent Exp: {curr_exp:,}/{next_level_exp[str(curr_level)]:,}\n\n__Inventory__\n{mystic_count:,}x Mystic\n{fine_count:,}x Fine\n{normal_count:,}x Enhancement", inline=True)

		start_mystic_count = mystic_count
		start_fine_count = fine_count
		start_normal_count = normal_count

		total_fine_refunded = 0
		total_normal_refunded = 0

		while mystic_count + fine_count + normal_count > 0 and curr_level < goal_level:
			prev_mystic_count = mystic_count
			prev_fine_count = fine_count	
			prev_normal_count = normal_count

			curr_upper_level_cap = 0

			for level_cap in ASCENSION_MILESTONES:
				if level_cap > curr_level:
					curr_upper_level_cap = level_cap
				else:
					break

			level_upto = curr_upper_level_cap
			if goal_level < curr_upper_level_cap:
				level_upto = goal_level
			
			# Add exp
			new_level, new_exp, mystic_count, fine_count, normal_count, fine_ore_refunded, normal_ore_refunded, wasted_exp = self.add_exp(next_level_exp, curr_level, level_upto, curr_exp, mystic_count, fine_count, normal_count)			

			total_fine_refunded += fine_ore_refunded
			total_normal_refunded += normal_ore_refunded

			embed_msg.add_field(name=f"**Leveling: {curr_level} -> {level_upto}**", value=f"Reached level {new_level:,}/{curr_upper_level_cap:,}\nCurrent exp: {new_exp:,}/{next_level_exp[str(new_level)]:,}", inline=True)
			embed_msg.add_field(name=f"**Used**", value=f"{prev_mystic_count - mystic_count}x Mystic\n{prev_fine_count - fine_count +fine_ore_refunded}x Fine\n{prev_normal_count - normal_count + normal_ore_refunded}x Enhancement", inline=True)
			embed_msg.add_field(name=f"**Refunded**", value=f"{fine_ore_refunded}x Fine\n{normal_ore_refunded}x Enhancement", inline=True)

			curr_level = new_level
			curr_exp = new_exp
		
		msg = f"__Weapon__\nWeapon rarity: {rarity}:star:\nWeapon level: {curr_level}\nCurrent Exp: {curr_exp:,}/{next_level_exp[str(curr_level)]:,}\n\n"
		msg += f"__Inventory__\n{mystic_count:,}x Mystic\n{fine_count:,}x Fine\n{normal_count:,}x Enhancement"
		embed_msg.insert_field_at(index=1, name="**After**", value=msg, inline=True)		
		
		if curr_level >= goal_level:
			msg = f"You have enough enhancement ores to reach level {goal_level}.\n\n"
		else:
			msg = f"You do not have enough enhancement ores to reach level {goal_level}.\n\n"
		msg += f"__Total used__\n{start_mystic_count - mystic_count}x Mystic\n{start_fine_count - fine_count + total_fine_refunded}x Fine\n{start_normal_count - normal_count + total_normal_refunded}x Enhancement\n\n"
		msg += f"__Total refunded__\n{total_fine_refunded}x Fine\n{total_normal_refunded}x Enhancement\n"
		embed_msg.insert_field_at(index=2, name="**Summary**", value=msg, inline=False)

		return embed_msg

	# Input: 
	# current level, goal level, current exp, and number of mystic, fine and regular ores.
	# Output: 
	# If enough then how many ores it will cost.
	# If not enough then what level will using all of the ores will get to and how many more ores needed to reach goal.
	@commands.command(aliases=["wep_exp"])
	async def weapon_exp_calculator(self, ctx, rarity, curr_level, goal_level, curr_exp, mystic_count, fine_count, normal_count):
		args = ctx.message.content.split()

		if len(args) == 8:
			try:
				rarity = int(rarity)
				curr_level = int(curr_level)
				goal_level = int(goal_level)
				curr_exp = int(curr_exp)
				mystic_count = int(mystic_count)
				fine_count = int(fine_count)
				normal_count = int(normal_count)
			except ValueError:
				raise commands.ArgumentParsingError(message="Please enter integer values only.")

			if not rarity in [5, 4, 3, 2, 1]:
				raise commands.ArgumentParsingError(message="Please enter a valid weapon rarity value.")

			if curr_level > goal_level:
				raise commands.ArgumentParsingError(message="Please enter current level and goal level where current level is less than goal level.")

			if mystic_count < 0 or fine_count < 0 or normal_count < 0:
				raise commands.ArgumentParsingError(message="Please enter number of enhancement ores greater or equal to 0.")

			embed_msg = discord.Embed(title=f"**{self.client.user.name}**", colour=discord.Colour.teal())
			embed_msg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			embed_msg = self.calculate(embed_msg, rarity, curr_level, goal_level, curr_exp, mystic_count, fine_count, normal_count)
			await ctx.send(embed=embed_msg)

		else:
			await ctx.send(f"Usage: {self.client.command_prefix}weapon_exp <rarity> <curr_level> <goal_level> <curr_exp> <mystic_count> <fine_count> <normal_count>\n{self.client.command_prefix}help for more details.")

def setup(client):
	client.add_cog(WeaponExpCalculator(client))