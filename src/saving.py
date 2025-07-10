import os, pickle, json
from Constants import *
from item import Item
from player import Player
from shop import Shop
from dungeon import Dungeon

SAVE_DIR = '../saves'
SAVE_SLOTS_SUMMARY_FILE = os.path.join(SAVE_DIR, 'save_slots.json')

def save_game(player: Player, shop: Shop, dungeon: Dungeon, save_slot: int):
    # Ensure the save directory exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    save_name = f'slot{save_slot}'
    json_data = list_saves_summary()
    if save_name in json_data:
        prompt = f"A save already exists in slot {save_slot}. Would you like to overwrite?\n1 = Yes\n2 = No"
        choice = validate_input(prompt, ["1", "2"])
        if choice == "2":
            print("Save cancelled.")
            return True

    save_data = {
        'player': player,
        'shop': shop,
        'dungeon': dungeon
    }
    save_path = os.path.join(SAVE_DIR, f'{save_name}.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(save_data, f)
    
    json_data[save_name] = {
        "player": player.name,
        "class": player.style,
        "level": player.level,
        "dungeon": dungeon.name
    }

    save_saves_summary(json_data)
    print(f"Game saved successfully as '{save_name}'.")
    return False

def load_game(save_slot: int):
    save_name = f'slot{save_slot}'
    # Load the game state from a file
    save_path = os.path.join(SAVE_DIR, f'{save_name}.pkl')
    if not os.path.exists(save_path):
        print(f"No saved game found with the name '{save_name}'.")
        return False, None, None, None
    
    with open(save_path, 'rb') as f:
        save_data = pickle.load(f)
    
    player = save_data['player']
    shop = save_data['shop']
    dungeon = save_data['dungeon']
    
    print(f"Game '{save_name}' loaded successfully.")
    return True, player, shop, dungeon

def list_saves_summary():
    # Load the save slots summary from JSON
    if not os.path.exists(SAVE_SLOTS_SUMMARY_FILE):
        return {}

    with open(SAVE_SLOTS_SUMMARY_FILE, 'r') as f:
        return json.load(f)
    
def save_saves_summary(data):
    # Save the save slots summary to JSON
    with open(SAVE_SLOTS_SUMMARY_FILE, 'w') as f:
        json.dump(data, f, indent=4)