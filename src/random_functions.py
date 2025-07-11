import random, time
from Constants import *
from player import Player
from Enemy import Enemy
from dungeon import Dungeon
from shop import Shop, user_yes_no_check
from characters import get_starting_stats
from item import Item

def create_dungeon(player: Player):
    type = random.choice(dungeon_types)
    info_list = dungeon_type_info[type]
    diff = 1

    if player.level <= 4:
        floors = 1
        rooms = random.randint(4, 7)
    elif 4 < player.level <= 9:
        floors = 2
        rooms = random.randint(2, 4)
        diff = 2
    elif 9 < player.level <= 20:
        floors = 3
        rooms = random.randint(2, 4)
        diff = 3
    else:
        floors = 4
        rooms = 3
        diff = 4

    return Dungeon(type, floors, diff, info_list, player.level, rooms)

def create_character():
    random_stats = get_starting_stats()
    name = input("Character Name: ")
    while name == "":
        print("Please enter a name.")
        name = input()
    print(divider)

    char_type = validate_input("Choose class type:\n1 = Mage\n2 = Archer\n3 = Warrior",
                               ["1","2","3"],
                               "Please choose a valid class.")
    
    match char_type:
        case "1": #Mage
            char_type = "Mage"
            prompt = "Choose starting spell:\n1 = Fireball\n2 = Chain Lightning\n3 = Shadow Fangs"
            valid = ["1", "2", "3"]
            starting_spell_num = validate_input(prompt, valid, "Please choose a valid starting spell.")

            match starting_spell_num:
                case "1":
                    starting_spell = "Fireball"
                case "2":
                    starting_spell = "Chain Lightning"
                case _:
                    starting_spell = "Shadow Fangs"

            char = Player(name, random_stats, style = "Mage", skills= [], spells=[starting_spell])
        
        case "2": #Archer
            char_type = "Archer"
            prompt = "Choose a starting skill:\n1 = Double Shot\n2 = Piercing Shot"
            valid = ["1", "2"]
            starting_skill_num = validate_input(prompt, valid, "Please choose a valid starting skill.")

            match starting_skill_num:
                case "1":
                    starting_skill = "Double Shot"
                case _:
                    starting_skill = "Piercing Shot"

            char = Player(name, random_stats, style="Archer", skills=[starting_skill])

        case _: #Warrior
            char_type = "Warrior"
            prompt = "Choose a starting skill:\n1 = Devastating Strike\n2 = Cleave\n3 = Fury of Blows\n4 = Draining Strike"
            valid = ["1", "2", "3", "4"]
            starting_skill_num = validate_input(prompt, valid, "Please choose a valid starting skill.")
            
            match starting_skill_num:
                case "1":
                    starting_skill = "Devastating Strike"
                case "2":
                    starting_skill = "Cleave"
                case "3":
                    starting_skill = "Fury of Blows"
                case _:
                    starting_skill = "Draining Strike"

            char = Player(name, random_stats, style="Warrior", skills=[starting_skill])
    
    return char

def check_load(player, shop, dungeon):
    if not isinstance(player, Player):
        print("Error: Player data is invalid.")
        return False
    if not isinstance(shop, Shop):
        print("Error: Shop data is invalid.")
        return False
    if not isinstance(dungeon, Dungeon):
        print("Error: Dungeon data is invalid.")
        return False
    return True

def use_item(player: Player, item: Item):
    match item.name:
        case "HEALTH POTION":
            if item.quantity > 0:
                if user_yes_no_check(item.name, "use"):
                    item.quantity -= 1
                    player.health = player.max_health
                    print("Drinking health potion...")
                    print(f"Health recovered! {player.name} now has {player.health} health.")
        case "MANA POTION":
            if item.quantity > 0:
                if user_yes_no_check(item, "use"):
                    item.quantity -= 1
                    player.mana = player.max_mana
                    print("Drinking mana potion...")
                    print(f"Mana recovered! {player.name} now has {player.mana} mana.")
        case "SPELLBOOK":
            spell_list = spells.copy()
            if item.quantity > 0:
                if user_yes_no_check(item, "use"):
                    for spell in player.spells:
                        spell_list.remove(spell)
                    if len(spell_list) == 0:
                        print("No more spells to learn.")
                        return 
                    new_spell = random.choice(spell_list)
                    player.learn_spell(new_spell)
                    item.quantity -= 1
        case "SKILLBOOK":
            skill_list = skills.copy()
            if item.quantity > 0:
                if user_yes_no_check(item, "use"):
                    
                    for skill in player.skills:
                        skill_list.remove(skill)
                    if player.style != "Archer":
                        skill_list.remove("Double Shot")
                        skill_list.remove("Piercing Shot")
                    if len(skill_list) == 0:
                        print("No more skills to learn.")
                        return 
                    new_skill = random.choice(skill_list)
                    player.learn_skill(new_skill)
                    item.quantity -= 1
        case "COINS":
            print("Lovely money!")
        case _:
            if "FRUIT OF " in item.name:
                if item.quantity > 0:
                    if user_yes_no_check(item, "use"):
                        stat = item.name[len("FRUIT OF "):]
                        value = random.randint(1, 5)

                        match stat:
                            case "STRENGTH":
                                player.strength += value
                            case "AGILITY":
                                player.agility += value
                            case "CONSTITUTION":
                                player.constitution += value
                            case "WISDOM":
                                player.wisdom += value
                            case "LUCK":
                                player.luck += value
                            case "ASCENSION":
                                player.growth += random.randint(1, 2)
                            case "BLOODTHIRST":
                                player.lifesteal += 2 * value
                        item.quantity -= 1
            else:
                print("I wonder what I can do with this... Maybe I can sell it?")

    exists, index = player.check_for_item(item.name)
    
    if exists and player.invent[index].quantity == 0:
        player.invent.remove(item)

    return

 