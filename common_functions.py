import discord
import math

def default_embed_template(ctx, title):
	msg = discord.Embed(title=f"**{title}**", colour=discord.Colour.teal())
	msg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	return msg

# total_exp_next_level: the exp to go from 0 exp at the current level to leveling up. 
def use_exp_mat(curr_exp: int, total_exp_next_level: int, material_count: int, exp_per_material: int, go_over: bool):
	
	exp_needed = total_exp_next_level - curr_exp

	# Whether to go over or under the total_exp_next_level 
	if exp_needed > 0:
		i = 0
		if go_over:
			i = 1

		material_used = 0

		if math.floor(exp_needed/exp_per_material) + i < material_count:
			material_used = math.floor(exp_needed/exp_per_material) + i
		else:
			material_used = material_count
		material_count -= material_used
		curr_exp += material_used*exp_per_material

	return curr_exp, material_count