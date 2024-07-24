import random
from characters import *
from equipment import *

def main():
    print("--------------------------------------------------------")
    print("Welcome to Fantasy Simulator".center(54))
    print("--------------------------------------------------------")

    random_stats = [random.randint(0,10),
                    random.randint(0,10),
                    random.randint(0,10),
                    random.randint(0,10),
                    random.randint(0,10),]
    name = input("Character Name: ")
    print("Choose class type:\n1 = Mage\n2 = Archer\n3 = Warrior")
    char_type = input()
    while not (char_type == "1" or char_type == "2" or char_type == "3"):
        print("Please choose a valid class.")
        char_type = input()
    
    if char_type == "1":
        print("Choose starting spell:\n1 = Fireball\n2 = Chain Lightning\n3 = Shadow Fangs")
        starting_spell = input()
        while not (starting_spell == "1" or starting_spell == "2" or starting_spell == "3"):
            print("Please choose a valid starting spell.")
            starting_spell = input()

        char = Mage(name, random_stats, starting_spell)

    elif char_type == "2":
        print("Choose a starting skill:\n1 = Double Shot\n2 = Piercing Shot")
        starting_skill = input()
        while not (starting_skill == "1" or starting_skill == "2"):
            print("Please choose a valid starting skill.")
            starting_skill = input()

        char = Archer(name, random_stats, starting_skill)
    elif char_type == "3":
        print("Choose a starting skill:\n1 = Devastating Strike\n2 = Cleave\n3 = Fury of Blows")
        starting_skill = input()
        while not (starting_skill == "1" or starting_skill == "2" or starting_skill == "3"):
            print("Please choose a valid starting skill.")
            starting_skill = input()

        char = Warrior(name, random_stats, starting_skill)
        
    print(char)
    print(char.invent)

main()