from random_functions import create_character, create_dungeon, check_load
from Menus import main_menu, load_menu
from shop import Shop, user_yes_no_check
from Constants import *
from saving import save_game, load_game

# Stats MUST be in the following order:
# [Strength, Agility, Constitution, Wisdom, Luck]

def main():
    print(divider)
    print("Welcome to Hero Quest".center(54))
    print(divider)

    prompt = "1 = Load Game\n2 = New Game"
    game = validate_input(prompt, ["1", "2"])

    if game == "1":
        success = False
        while not success:
            chosen_slot = load_menu()
            if chosen_slot == "0":
                print("Starting a new game.")
                print(divider)
                success = True
                player = create_character()
                print(f"Summary:\n{player}\nInventory:\n{player.invent}")
                print(divider)
                dungeon = create_dungeon(player)
                shop = Shop(2.5, player)
                continue
            success_load, player, shop, dungeon = load_game(int(chosen_slot))
            if success_load:
                success = check_load(player, shop, dungeon)
                if not success:
                    print("Error loading game. Please try again.")
                    print("If the problem persists, please start a new game as the save file is likely corrupted.")
                    print(divider)
            
    else:
        player = create_character()

        print(f"Summary:\n{player}\nInventory:\n{player.invent}")

        print(divider)
        dungeon = create_dungeon(player)
        shop = Shop(2.5, player)
        

    keep_playing = True

    while keep_playing:
        if len(dungeon) == 0: # type: ignore
            dungeon = create_dungeon(player) # type: ignore

        keep_playing = main_menu(player, dungeon, shop) # type: ignore

main()