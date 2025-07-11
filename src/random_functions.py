import random, time
from Constants import *
from player import Player
from Enemy import Enemy
from dungeon import Dungeon
from shop import Shop
from characters import get_starting_stats

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