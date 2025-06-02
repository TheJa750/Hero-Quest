import random, time
from characters import *
from equipment import *
from random_gens import *
from archer import *
from Warrior import *
from Mage import *

# Stats MUST be in the following order:
# [Strength, Agility, Constitution, Wisdom, Luck]

def main():
    divider = "--------------------------------------------------------"
    print(divider)
    print("Welcome to Fantasy Simulator".center(54))
    print(divider)

    char = create_character(divider)

    print(f"Summary:\n{char}\nInventory:\n{char.invent}")

    enemy = Enemy("Bones", [5,5,5,5,5], diff_modifier=1.5)
    print(enemy)

    """
    print(f"Testing battle: {char.name} vs {enemy.name}")
    print(divider)

    print("Begin!")
    #battle(char, enemy, divider)
    """

    print(divider)
    print(char.phys_damage)
    if char.get_class_type() == "Archer":
        char.basic_shot(enemy) #type: ignore
        char.double_shot(enemy) #type: ignore
        char.piercing_shot(enemy) #type: ignore

def battle(fighter1: Character, fighter2: Character, divider):
    #determine who goes first:
    if fighter1.agility > fighter2.agility:
        #fighter1 goes first
        first = "1"
    elif fighter1.agility < fighter2.agility:
        first = "2"
    else:
        first = random.choice(["1","2"])
    
    while fighter1.health > 0 and fighter2.health > 0:
        print(divider)
        if first == "1":
            fighter1.melee_strike(fighter2)
            if fighter2.health > 0:
                fighter2.melee_strike(fighter1)
            time.sleep(0.1)
        else:
            fighter2.melee_strike(fighter1)
            if fighter1.health > 0:
                fighter1.melee_strike(fighter2)
            time.sleep(0.1)
    
    print(divider)
    print("Battle Concluded")
    if fighter1.health > 0:
        print(f"The winner is {fighter1.name}")
    else:
        print(f"The winner is {fighter2.name}")

def create_character(divider):
    random_stats = get_starting_stats()
    name = input("Character Name: ")
    while name == "":
        print("Please enter a name.")
        name = input()
    print(divider)
    print("Choose class type:\n1 = Mage\n2 = Archer\n3 = Warrior")
    char_type = input()
    while not (char_type == "1" or char_type == "2" or char_type == "3"):
        print("Please choose a valid class.")
        char_type = input()
    
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