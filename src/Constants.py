#info variables have the following structure:
#info[0] = list of non-boss npc names/types
#info[1] = list of boss npc names/types

dwarven_info = []
undead_info = []
forest_info = []
tower_info = []

#Dwarven info:
dwarven_basic = [
    "Dwarf",
    "Simple Dwarven Golem",
    "Dwarven Warrior"
]

dwarven_bosses = [
    "City Defender Golem",
    "Dwarven King"
]
dwarven_info.append(dwarven_basic)
dwarven_info.append(dwarven_bosses)

#Undead info:
undead_basic = [
    "Zombie",
    "Skeleton",
    "Ghoul",
    "Revenant",
    "Wight"
]

undead_bosses = [
    "Draugr",
    "Flesh Abomination",
    "Death Knight"
]

undead_info.append(undead_basic)
undead_info.append(undead_bosses)

#Forest info:
forest_basic = [
    "Wolf",
    "Bear",
    "Snake",
    "Giant Bee",
    "Goblin"
]

forest_bosses = [
    "Druid",
    "Troll",
    "Dryad"
]

forest_info.append(forest_basic)
forest_info.append(forest_bosses)

#Tower info:
tower_basic = [
    "Giant Bat",
    "Rock Elemental",
    "Bandit",
    "Floating Sword"
]

tower_bosses = [
    "Bandit Leader",
    "Demon",
    "Dragon"
]

tower_info.append(tower_basic)
tower_info.append(tower_bosses)

dungeon_types = [
    "Dwarven",
    "Undead",
    "Forest",
    "Tower"
]

dungeon_type_info = {
    "Dwarven" : dwarven_info,
    "Undead" : undead_info,
    "Forest" : forest_info,
    "Tower" : tower_info
}