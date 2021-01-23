import discord
import json
import math
import time

from discord.ext import commands

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
			difference = int(next_level_exp[str(curr_level)]) - curr_exp
			
			# Use mystic enhancement ores
			if difference > 0:
				ore_used = 0
				if math.floor(difference/MYSTIC) + 1 < mystic_count:
					ore_used = math.floor(difference/MYSTIC) + 1
				else:
					ore_used = mystic_count
				curr_exp += ore_used*MYSTIC
				mystic_count -= ore_used
				difference -= ore_used*MYSTIC

			# Use fine enhancement ores
			if difference > 0:
				ore_used = 0
				if math.floor(difference/FINE) + 1 < fine_count:
					ore_used = math.floor(difference/FINE) + 1
				else:
					ore_used = fine_count
				curr_exp += ore_used*FINE
				fine_count -= ore_used
				difference -= ore_used*FINE

			# Use normal enhancement ores
			if difference > 0:
				ore_used = 0
				if math.floor(difference/NORMAL) + 1 < normal_count:
					ore_used = math.floor(difference/NORMAL) + 1
				else:
					ore_used = normal_count
				curr_exp += ore_used*NORMAL
				normal_count -= ore_used
				difference -= ore_used*NORMAL

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
		with open(f"./cogs/wep_{rarity}_star_next_level_exp.json", "r") as f:
			next_level_exp = json.load(f)
		f.close()

		if curr_exp > int(next_level_exp[str(curr_level)]):
			raise commands.ArgumentParsingError(message="Invalid current weapon experience points value.")

		curr_mystic_count = mystic_count
		curr_fine_count = fine_count
		curr_normal_count = normal_count

		total_fine_refunded = 0
		total_normal_refunded = 0

		print("ASDASASFGAG")

		while curr_mystic_count + curr_fine_count + curr_normal_count > 0:
			curr_upper_lvl_cap = 0

			for lvl_cap in ASCENSION_MILESTONES:
				if lvl_cap > curr_level:
					curr_upper_lvl_cap = lvl_cap
				else:
					break

			level_upto = curr_upper_lvl_cap
			if goal_level < curr_upper_lvl_cap:
				level_upto = goal_level
			
			# Add exp
			new_level, new_exp, curr_mystic_count, curr_fine_count, curr_normal_count, fine_ore_refunded, normal_ore_refunded, wasted_exp = self.add_exp(next_level_exp, curr_level, level_upto, curr_exp, curr_mystic_count, curr_fine_count, curr_normal_count)			

			total_fine_refunded += fine_ore_refunded
			total_normal_refunded += normal_ore_refunded

			msg = f"""
			----\n
			current weapon lvl = {new_level}\n
			current weapon exp = {new_exp}\n

			original mystic count = {mystic_count}\n
			current mystic count = {curr_mystic_count} \n
			total used mystic count = {mystic_count - curr_mystic_count} \n

			original fine count = {fine_count}\n
			current fine count = {curr_fine_count} \n
			fine ore refunded this round = {fine_ore_refunded} \n
			total used fine ore = {fine_count - curr_fine_count + total_fine_refunded}\n 

			original normal count = {normal_count} \n 
			current normal count = {curr_normal_count} \n
			normal ore refunded this round = {normal_ore_refunded} \n
			total used normal ore = {normal_count - curr_normal_count + total_normal_refunded}\n
			
			wasted exp = {wasted_exp}\n
			total fine refunded = {total_fine_refunded}\n
			total normal refunded = {total_normal_refunded}\n
			----\n
			"""
			print(msg)
			
			curr_level = new_level
			curr_exp = new_exp
		
			if curr_level == goal_level:
				break
		return embed_msg

	# Input: current level, goal level, current exp, and number of mystic, fine and regular ores.
	# Output: If enough then how much it will cost
	# 		: if not enough then what using all of the ores will get to and how many more mystic ores needed to reach goal
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

			embed_msg = discord.Embed(title="Unital Bot", colour=discord.Colour.teal())
			embed_msg.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			embed_msg.add_field(name="Before", value=f"Weapon rarity: {rarity}*\nWeapon level: {curr_level}\nGoal level: {goal_level}\nCurrent Xp: {curr_exp}\n# of Mystic enhancement ores: {mystic_count}\n# of Fine enhancement ores: {fine_count}\n# of Enhancement ores: {normal_count}")

			embed_msg = self.calculate(embed_msg, rarity, curr_level, goal_level, curr_exp, mystic_count, fine_count, normal_count)
			await ctx.send(embed=embed_msg)

		else:
			await ctx.send(f"Usage: {self.client.command_prefix}weapon_exp <rarity> <curr_level> <goal_level> <curr_exp> <mystic_count> <fine_count> <normal_count>\n{self.client.command_prefix}help for more details.")


def setup(client):
	client.add_cog(WeaponExpCalculator(client))