import discord
import json

from discord.ext import commands
from common_functions import default_embed_template, use_exp_mat

HERO_WIT = 20000
ADVENTURER_EXPERIENCE = 5000
WANDER_ADVICE = 1000
ASCENSION_MILESTONES = [90, 80, 70, 60, 50, 40, 20]


class CharacterExpCalculator(commands.Cog):
	def __init__(self, client):
		self.client = client

	def format_char_stats(self, curr_level, curr_exp, curr_exp_cap, herowit_count, advexp_count, wandadv_count):
		msg = f"__Character__\nCharacter level: {curr_level}\n"
		msg += f"Current Exp: {curr_exp:,}/{curr_exp_cap:,}\n\n"
		msg += f"__Inventory__\n"
		msg += f"{herowit_count:,}x Hero's Wit\n"
		msg += f"{advexp_count:,}x Adventurer's Experience\n"
		msg += f"{wandadv_count:,}x Wanderer's Advice\n"
		return msg

	def add_exp(self, next_level_exp, curr_level, level_upto, curr_exp, herowit_count, advexp_count, wandadv_count):
		wasted_exp = 0

		while herowit_count + advexp_count + wandadv_count > 0 and curr_level < level_upto:
			difference = int(next_level_exp[str(curr_level)]) - curr_exp
			
			curr_exp, herowit_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, herowit_count, HERO_WIT, False)
			curr_exp, advexp_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, advexp_count, ADVENTURER_EXPERIENCE, False)
			curr_exp, wandadv_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, wandadv_count, WANDER_ADVICE, False)

			curr_exp, wandadv_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, wandadv_count, WANDER_ADVICE, True)
			curr_exp, herowit_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, herowit_count, HERO_WIT, True)
			curr_exp, advexp_count = use_exp_mat(curr_exp, int(next_level_exp[str(curr_level)]) - curr_exp, advexp_count, ADVENTURER_EXPERIENCE, True)

			# Calculate exp overflow
			while True:
				if curr_exp >= int(next_level_exp[str(curr_level)]):
					if curr_level + 1 in ASCENSION_MILESTONES:
						# Calculate refunded ores if any
						wasted_exp = curr_exp - int(next_level_exp[str(curr_level)])

						curr_exp = 0
						curr_level += 1

						return curr_level, curr_exp, herowit_count, advexp_count, wasted_exp
					else:
						curr_exp = curr_exp - int(next_level_exp[str(curr_level)])
						curr_level += 1
				else:
					break
		return curr_level, curr_exp, herowit_count, advexp_count, wandadv_count, wasted_exp


	def calculate(self, embed_msg, curr_level, goal_level, curr_exp, herowit_count, advexp_count, wandadv_count):
		with open("./char_exp_per_level/char_exp_per_level.json", "r") as f:
			next_level_exp = json.load(f)
		f.close()
		
		if not str(curr_level) in next_level_exp:
			raise commands.ArgumentParsingError(message="Please enter a valid character level.")

		if not str(goal_level) in next_level_exp:
			raise commands.ArgumentParsingError(message="Please enter a valid character level.")	

		if curr_exp > int(next_level_exp[str(curr_level)]):
			raise commands.ArgumentParsingError(message="Invalid current character experience points value.")

		msg = self.format_char_stats(curr_level, curr_exp, next_level_exp[str(curr_level)], herowit_count, advexp_count, wandadv_count)
		embed_msg.add_field(name="**Before**", value=msg, inline=True)

		start_herowit_count = herowit_count
		start_advexp_count = advexp_count
		start_wandadv_count = wandadv_count

		while herowit_count + advexp_count + wandadv_count > 0 and curr_level < goal_level:
			prev_herowit_count = herowit_count
			prev_advexp_count = advexp_count
			prev_wandadv_count = wandadv_count

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
			new_level, new_exp, herowit_count, advexp_count, wandadv_count, wasted_exp = self.add_exp(next_level_exp, curr_level, level_upto, curr_exp, herowit_count, advexp_count, wandadv_count)			

			embed_msg.add_field(name=f"**Leveling: {curr_level} -> {level_upto}**", value=f"Reached level {new_level:,}/{curr_upper_level_cap:,}\nCurrent exp: {new_exp:,}/{next_level_exp[str(new_level)]:,}", inline=True)
			embed_msg.add_field(name=f"**Used**", value=f"{prev_herowit_count - herowit_count}x Hero's Wit\n{prev_advexp_count - advexp_count}x Adventurer's Experience\n{prev_wandadv_count - wandadv_count}x Wanderer's Advice", inline=True)

			curr_level = new_level
			# Temp Line
			# curr_level = goal_level
			curr_exp = new_exp

		msg = self.format_char_stats(curr_level, curr_exp, next_level_exp[str(curr_level)], herowit_count, advexp_count, wandadv_count)
		embed_msg.insert_field_at(index=1, name="**After**", value=msg, inline=True)			

		if curr_level >= goal_level:
			msg = f"You have enough materials to reach level {goal_level}.\n\n"
		else:
			msg = f"You do not have enough materials to reach level {goal_level}.\n\n"
		msg += f"__Total used__\n{start_herowit_count - herowit_count}x Hero's Wit\n{start_advexp_count - advexp_count}x Adventurer's Experience\n{start_wandadv_count - wandadv_count}x Wanderer's Advice\n\n"
		embed_msg.insert_field_at(index=2, name="**Summary**", value=msg, inline=False)

		return embed_msg

	@commands.command(aliases=["char_exp"])
	async def character_exp_calculator(self, ctx, curr_level, goal_level, curr_exp, herowit_count, advexp_count, wandadv_count):
		args = ctx.message.content.split()

		if len(args) == 7:
			try:
				curr_level = int(curr_level)
				goal_level = int(goal_level)
				curr_exp = int(curr_exp)
				herowit_count = int(herowit_count)
				advexp_count = int(advexp_count)
				wandadv_count = int(wandadv_count)
			except ValueError:
				raise commands.ArgumentParsingError(message="Please enter integer values only.")

			if curr_level > goal_level:
				raise commands.ArgumentParsingError(message="Please enter current level and goal level where current level is less than goal level.")

			if herowit_count < 0 or advexp_count < 0 or wandadv_count < 0:
				raise commands.ArgumentParsingError(message="Please enter number of materials equal to or greater than 0.")

			embed_msg = default_embed_template(ctx, self.client.user.name)
			embed_msg = self.calculate(embed_msg, curr_level, goal_level, curr_exp, herowit_count, advexp_count, wandadv_count)

			await ctx.send(embed=embed_msg)

		else:
			await ctx.send(f"Usage: {self.client.command_prefix}char_exp <curr_level> <goal_level> <curr_exp> <herowit_count> <advexp_count> <wandadv_count>\n{self.client.command_prefix}help for more details.")

def setup(client):
	client.add_cog(CharacterExpCalculator(client))