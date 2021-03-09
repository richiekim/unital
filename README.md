# GenshinCalc

Fan-made bot for Genshin Impact related calculations.

## Commands

### Weapon EXP Calculator

Calculates if you have enough Enhancement Ores to level up your weapon to a specific level, how much resources are used per level milestone and how much you have left after leveling. If not enough, it will also tell you what level you will reach if you use all of your materials. Ore refunds are accounted for in the calculation.

```
!wep_exp <rarity> <curr_level> <goal_level> <curr_exp> <mystic_count> <fine_count> <normal_count>
```
<rarity>  
* Rarity of the weapon
* Accepts values from 1 to 5  

<curr_level>
* Current level of the weapon

<goal_level>  
* Level you want to level the weapon to
* Must be greater than <curr_level>

<curr_exp>
* Current EXP of the weapon

<mystic_count> 
* Number of Mystic Enhancement Ores in your inventory

<fine_count>
* Number of Fine Enhancement Ores in your inventory

<normal_count>  
* Number of Enhancement Ores in your inventory

### Character EXP Calculator

Calculates if you have enough EXP material to level up your character is a specific level, how much resources are used per level milestone and how much you have after leveling. If not enough, it will also tell you what level you will reach if you use all of your materials.

```
!char_exp <curr_level> <goal_level> <curr_exp> <herowit_count> <advexp_count> <wandadv_count>
```

<curr_level>
* Current level of the character

<goal_level>
* Level you want to level the character to
* Must be greater than <curr_level>

<curr_exp>
* Current EXP of the character

<herowit_count>
* Number of Hero's Wits in your inventory

<advexp_count>
* Number of Adventurer's Experience in your inventory

<wanadv_count>
* Number of Wanderer's Advice in your inventory

## TODO
* Ascension material calculator for weapons
* Ascension material calculator for characters

## License
[MIT](https://choosealicense.com/licenses/mit/)