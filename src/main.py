import random, time
from characters import *
from equipment import *
from random_functions import *
from Menus import *
from dungeon import *

# Stats MUST be in the following order:
# [Strength, Agility, Constitution, Wisdom, Luck]

def main():
    print(divider)
    print("Welcome to Fantasy Simulator".center(54))
    print(divider)

    player = create_character()

    print(f"Summary:\n{player}\nInventory:\n{player.invent}")

    print(divider)

    while True:
        keep_playing = main_menu(player)

        if not keep_playing:
            break

        

def battle(player: Character, enemies: list):
    #Need some logic determining battle order, for now player will always go first so that I can make the battle loop work
    
    #Main battle loop, if player is alive and at least 1 enemy is alive battle continues
    while player.health > 0 and len(enemies) > 0:


        action_code = main_combat_menu(player, enemies)
        print(divider)

        if action_code != 0:
            print(f"{player.name} has fled succesfully.")
            break

        for enemy in enemies:
            if enemy.health <= 0:
                enemies.remove(enemy)

        if len(enemies) > 0:
            for enemy in enemies:
                time.sleep(0.25)
                enemy.melee_strike(player)
                print(divider)
                if player.health <= 0:
                    break

    print(divider)
    print("Battle Concluded")
    if player.health > 0:
        print(f"The winner is {player.name}.")
    else:
        print("You have died.")
        print("Thank you for playing Fantasy Simulator!")

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

            char = Character(name, random_stats, style = "Mage", skills= [], spells=[starting_spell])
        
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

            char = Character(name, random_stats, style="Archer", skills=[starting_skill])

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

            char = Character(name, random_stats, style="Warrior", skills=[starting_skill])
    
    return char

def create_dungeon(player):
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

    return Dungeon(type, floors, 1, info_list, 3)

main()