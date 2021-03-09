class HelpText:
	def __init__(self):
		self._description = {
			"char_exp": "Calculates if you have enough character EXP material to level up your weapon to a specific level, how much of your resources are used per level milestone and how much you have left after leveling. If not enough, it will also tell you what level you will reach when you use all of your materials. Ore refunds are accounted for in the calculation.",
			"wep_exp": "Calculates if you have enough weapon EXP material to level up your character is a specific level, how much of your resources are used per level milestone and how much you have left after leveling. If not enough, it will also tell you what level you will reach when you use all of your materials."
		}

		self._usage = {
			"char_exp": "`!char_exp <curr_level> <goal_level> <curr_exp> <herowit_count> <advexp_count> <wandadv_count>`",
			"wep_exp": "`!wep_exp <rarity> <curr_level> <goal_level> <curr_exp> <mystic_count> <fine_count> <normal_count>`"
		}

		self._details = {
			"char_exp": "`<curr_level>`\nCurrent level of the character\n\n`<goal_level>`\nLevel you want to level the character to\nMust be greater than `<curr_level>`\n\n`<curr_exp>`\nCurrent EXP of the character\n\n`<herowit_count>`\nNumber of Hero's Wits in your inventory\n\n`<advexp_count>`\nNumber of Adventurer's Experience in your inventory\n\n`<wanadv_count>`\nNumber of Wanderer's Advice in your inventory",
			"wep_exp": "`<rarity>`\nRarity of the weapon\nAccepts values from 1 to 5\n\n`<curr_level>`\nCurrent level of the weapon\n\n`<goal_level>`\nLevel you want to level the weapon to\nMust be greater than `<curr_level>`\n\n`<curr_exp>`\nCurrent EXP of the weapon\n\n`<mystic_count>`\nNumber of Mystic Enhancement Ores in your inventory\n\n`<fine_count>`\nNumber of Fine Enhancement Ores in your inventory\n\n`<normal_count>`\nNumber of Enhancement Ores in your inventory"
		}

	@property
	def description(self):
		return self._description

	@property
	def usage(self):
		return self._usage

	@property
	def details(self):
		return self._details
