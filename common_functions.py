import discord
import math

def default_embed_template(ctx, title):
	msg = discord.Embed(title=f"**{title}**", colour=discord.Colour.teal())
	msg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	return msg

def use_exp_mat(curr_exp: int, exp_required: int, material_count: int, exp_per_material: int, go_over: bool):
	# Whether to go over the exp_required 
	i = 0
	if go_over:
		i = 1

	material_used = 0

	if math.floor(exp_required/exp_per_material) + i < material_count:
		material_used = math.floor(exp_required/exp_per_material) + 1
	else:
		material_used = material_count
	material_count -= material_used
	curr_exp += material_used*exp_per_material

	return curr_exp, material_count