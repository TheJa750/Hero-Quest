from random_functions import create_character, create_dungeon
from Menus import main_menu
from shop import Shop
from Constants import *

# Stats MUST be in the following order:
# [Strength, Agility, Constitution, Wisdom, Luck]

def main():
    print(divider)
    print("Welcome to Fantasy Simulator".center(54))
    print(divider)

    player = create_character()

    print(f"Summary:\n{player}\nInventory:\n{player.invent}")

    print(divider)
    dungeon = create_dungeon(player)
    shop = Shop(
        ["HEALTH POTION", "MANA POTION"],
        {"HEALTH POTION": 50, "MANA POTION": 50},
        []
    )

    keep_playing = True

    while keep_playing:
        if len(dungeon) == 0:
            dungeon = create_dungeon(player)

        keep_playing = main_menu(player, dungeon, shop)


    #Add save data here if possible.

main()