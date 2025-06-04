import random, time
from characters import *
from equipment import *
from random_functions import *
from archer import *
from Warrior import *
from Mage import *
from Menus import *

# Stats MUST be in the following order:
# [Strength, Agility, Constitution, Wisdom, Luck]

def main():
    print(divider)
    print("Welcome to Fantasy Simulator".center(54))
    print(divider)

    char = create_character()

    print(f"Summary:\n{char}\nInventory:\n{char.invent}")


    print(divider)
    enemy_list = []
    for i in range(random.randint(1,4)):
        stats = get_starting_stats(random.randint(30,40))
        enemy = Enemy(f"Enemy {i+1}", stats)
        enemy_list.append(enemy)

    for enemy in enemy_list:
        print(enemy)

    main_combat_menu(char, enemy_list)


def battle(player: Character, enemies: list):
    
    
    while player.health > 0 and len(enemies) > 0:
        print(divider)

    
    print(divider)
    print("Battle Concluded")
    if player.health > 0:
        print(f"The winner is {player.name}")
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

            char = Mage(name, random_stats, [starting_spell])
        
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

            char = Archer(name, random_stats, [starting_skill])

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

            char = Warrior(name, random_stats, [starting_skill])
    
    return char

main()