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

    if player.level <= 4:
        floors = 1
    elif 4 < player.level <= 9:
        floors = 2
    elif 9 < player.level <= 20:
        floors = 3
    else:
        floors = 4 

    return Dungeon(type, floors, 1, info_list, player.level)

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
            print(divider)
            print("Choose starting spell:\n1 = Fireball\n2 = Chain Lightning\n3 = Shadow Fangs")
            starting_spell_num = input()
            while not (starting_spell_num == "1" or starting_spell_num == "2" or starting_spell_num == "3"):
                print("Please choose a valid starting spell.")
                starting_spell_num = input()

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
            print(divider)
            print("Choose a starting skill:\n1 = Double Shot\n2 = Piercing Shot")
            starting_skill_num = input()
            while not (starting_skill_num == "1" or starting_skill_num == "2"):
                print("Please choose a valid starting skill.")
                starting_skill_num = input()

            match starting_skill_num:
                case "1":
                    starting_skill = "Double Shot"
                case _:
                    starting_skill = "Piercing Shot"

            char = Player(name, random_stats, style="Archer", skills=[starting_skill])

        case _: #Warrior
            char_type = "Warrior"
            print(divider)
            print("Choose a starting skill:\n1 = Devastating Strike\n2 = Cleave\n3 = Fury of Blows")
            starting_skill_num = input()
            while not (starting_skill_num == "1" or starting_skill_num == "2" or starting_skill_num == "3"):
                print("Please choose a valid starting skill.")
                starting_skill_num = input()
            
            match starting_skill_num:
                case "1":
                    starting_skill = "Devastating Strike"
                case "2":
                    starting_skill = "Cleave"
                case _:
                    starting_skill = "Fury of Blows"

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