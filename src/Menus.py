import random, time
from player import Player
from dungeon import Dungeon, Room
from equipment import create_new_equipment, Equipment
from Constants import *
from Enemy import Enemy
from shop import Shop
from item import Item
from saving import list_saves_summary, save_game, delete_save
from dev_menu import dev_menu
from random_functions import use_item

def target_selection_menu(enemies: list):
    i = 1
    strings = ["Select an enemy to attack:", "0 = Back"]
    valid_inputs = ["0"]
    for enemy in enemies:
        strings.append(f"{i} = {enemy}")
        valid_inputs.append(f"{i}")
        i += 1
    prompt = "\n".join(strings)
    target = validate_input(prompt, valid_inputs)
    print(divider)

    return target

def skills_menu(player: Player,enemies: list):
    splash_skills = ["cleave"]
    while True:
        strings = ["Available Skills:", "0 = Back"]
        valid_inputs = ["0"]
        for i in range(1, len(player.skills) + 1):
            strings.append(f"{i} = {player.skills[i-1]}")
            valid_inputs.append(f"{i}")
        prompt = "\n".join(strings)
        choice = validate_input(prompt, valid_inputs)

        if choice == "0":
            return False
        else:
            target_str = target_selection_menu(enemies)
            if target_str != "0": #Target selected was not "Back"
                target = enemies[int(target_str)-1]
                skill_str = player.skills[int(choice) - 1].lower().replace(" ", "_")

                if skill_str in splash_skills:
                    if (int(target_str) - 2 >= 0) and enemies[int(target_str) - 2]:
                        target2 = enemies[int(target_str) - 2]
                    else:
                        target2 = None
                    if (int(target_str) < len(enemies)) and enemies[int(target_str)]:
                        target3 = enemies[int(target_str)]
                    else:
                        target3 = None
                    action_taken = player.__getattribute__(skill_str)(target, target2, target3)
                else:
                    action_taken = player.__getattribute__(skill_str)(target)
                
                if action_taken:
                    return True
                else:
                    return False

def spells_menu(player: Player,enemies: list):
    splash_spells = ["cast_chain_lightning"]
    while True:
        strings = ["Available Spells:", "0 = Back"]
        valid_inputs = ["0"]
        for i in range(1, len(player.spells) + 1):
            strings.append(f"{i} = {player.spells[i-1]}")
            valid_inputs.append(f"{i}")
        prompt = "\n".join(strings)
        choice = validate_input(prompt, valid_inputs)

        if choice == "0":
            return False
        else:
            target_str = target_selection_menu(enemies)
            if target_str != "0": #Target selected was not "Back"
                target = enemies[int(target_str)-1]
                spell_str = "cast_" + player.spells[int(choice) - 1].lower().replace(" ", "_")

                if spell_str in splash_spells: #spell can splash to other enemies
                    if (int(target_str) - 2 >= 0) and enemies[int(target_str) - 2]: #checking target left
                        target2 = enemies[int(target_str) - 2]
                    else:
                        target2 = None
                    if (int(target_str) < len(enemies)) and enemies[int(target_str)]: #checking target right
                        target3 = enemies[int(target_str)]
                    else:
                        target3 = None
                    action_taken = player.__getattribute__(spell_str)(target, target2, target3)
                else:
                    action_taken = player.__getattribute__(spell_str)(target)
                
                if action_taken:
                    return True
                else:
                    return False

def main_combat_menu(player: Player, enemies: list):
    while True:
        print(f"HP: {player.health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
        prompt = ("1 = Basic Attack\n2 = Skills\n3 = Spells\n4 = Flee")
        valid_inputs = ["1", "2", "3", "4"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "1": #Basic Attack - might need to check if player == archer and if so use basic_shot rather than melee_strike
                target_str = target_selection_menu(enemies)
                if target_str != "0":
                    target = enemies[int(target_str)-1]
                    if player.style == "Archer":
                        player.basic_shot(target)
                    else:
                        player.melee_strike(target)
                    return 0
                
            case "2": #Select skill
                action_taken = skills_menu(player, enemies)
                if action_taken:
                    return 0
                
            case "3": #Select spell
                action_taken = spells_menu(player, enemies)
                if action_taken:
                    return 0
            
            case "4": #Flee
                return 1
            
def main_menu(player: Player, current_dungeon: Dungeon, current_shop):
    while True:
        prompt = ("0 = Exit\n1 = Explore Dungeon\n2 = Inventory\n3 = Shop\n4 = Status\n5 = Manage Saved Games")
        valid_inputs = ["0", "1", "2", "3", "4", "5", "dev_menu"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "0":
                return False
            case "1":
                return dungeon_menu(player, current_dungeon, current_shop)
            case "2":
                prompt = ["Choose item:", "0 = Back"]
                valid_inputs = ["0"]
                
                for i in range(len(player.invent)):
                    prompt.append(f"{i+1} = {player.invent[i]}")
                    valid_inputs.append(f"{i+1}")

                choice = int(validate_input("\n".join(prompt), valid_inputs))

                if choice != 0:
                    item = player.invent[choice - 1]
                    use_item_menu(player, item)
                
                return True
            case "3":
                print(divider)
                shop_menu(player, current_shop)
                return True
            case "4":
                status_menu(player)
                return True
            case "5":
                return main_save_menu(player, current_shop, current_dungeon)
            case "dev_menu":
                return dev_menu(player, current_dungeon, current_shop)
            
def shop_menu(player: Player, shop: Shop):
    print("Welcome to the Fantasy Shop!")
    print("Can I interest you in any of our fine wares?")
    #print(f"Debug: markup is {shop.markup}")
    while True:

        prompt = ["0 = Back", "1 = Sell"]
        valid = ["0", "1"]

        for i in range(len(shop.items)):
            prompt.append(f"{i+2} = {shop.items[i]}")
            valid.append(f"{i+2}")

        choice = int(validate_input("\n".join(prompt), valid))

        match choice:
            case 0:
                return
            case 1:
                shopping = True
                while shopping:
                    shopping = shop.sell_item()
            case _:
                shop.buy_item(choice-2)
    
def use_item_menu(player:Player, item: Item):
    #print(divider)
    if item.is_equip:
        slot = item.item.slot
        match slot:
            case "head":
                player.head_armor.compare_equipment(item.item)
            case "body":
                player.body_armor.compare_equipment(item.item)
            case "weapon":
                player.weapon.compare_equipment(item.item)

        if user_yes_no_check(item.name, "equip"): 
            player.equip_item(item.item)
            player.invent.remove(item)
        else:
            return
        
    else:
        use_item(player, item)
        
        return
        
def user_yes_no_check(item, function: str):
    prompt = f"Would you like to {function} {item}?\n1 = Yes\n2 = No"
    choice = validate_input(prompt, ["1", "2"])

    if choice == "1":
        return True
    else:
        return False
    
def dungeon_menu(player: Player, dungeon: Dungeon, shop: Shop):
    print(divider)
    print(dungeon)
    

    keep_exploring = True

    while keep_exploring:
        room = dungeon.next_room() #type: Room | str

        if isinstance(room, str): #Only type str when dungeon complete, returns to main menu to begin new loop
            print(divider)
            print(room)
            shop.restock_items()
            return True
    
        print(divider)
        print(repr(room))
        print(divider)
        action_code = battle(player, room.enemies)

        match action_code:
            case 0:
                pass #Room has been cleared
            case 1: #Flee, return room to dungeon -> floor 0 -> room 0 then return to main menu with True (continue playing)
                dungeon.floors[0].rooms.insert(0, room.remove_dead_enemies())
                return True
            case 2: #player has died return to main menu with False (stop playing)
                player.death()
                return False
            
        room = dungeon.next_room() #type: Room | str

        if isinstance(room, str): #Only type str when dungeon complete, returns to main menu to begin new loop
            print(divider)
            print(room)
            shop.restock_items()
            return True
        else:
            dungeon.floors[0].rooms.insert(0, room)
        
        keep_exploring = user_yes_no_check(dungeon.name, "explore")

    return True
            
def battle(player: Player, enemies: list[Enemy]):
    #Need some logic determining battle order, for now player will always go first so that I can make the battle loop work
    
    #Main battle loop, if player is alive and at least 1 enemy is alive battle continues
    while player.health > 0 and len(enemies) > 0:


        action_code = main_combat_menu(player, enemies)
        #print(divider)

        if action_code != 0:
            print(f"{player.name} has fled succesfully.")
            return 1
        
        alive_enemies = []

        for enemy in enemies:
            if enemy.health <= 0:
                enemy.death(player)
            else:
                alive_enemies.append(enemy)

        enemies = alive_enemies

        if len(enemies) > 0:
            for enemy in enemies:
                time.sleep(0.5)
                print(divider)
                enemy.melee_strike(player)
                if player.health <= 0:
                    return 2

    return 0

def load_menu():
    strings = ["Available Save Slots:", "0 = Start New Game"]
    valid = ["0"]
    slots = []

    saves = list_saves_summary()
    i = 1
    for slot in saves:
        name = saves[slot]['player']
        style = saves[slot]['class']
        level = saves[slot]['level']
        dungeon = saves[slot]['dungeon']
        strings.append(f"{i} = {slot} [{name} - {style}, Level: {level}, Dungeon: {dungeon}]")
        valid.append(str(i))
        slots.append(slot)
        i += 1

    chosen_slot = validate_input("\n".join(strings), valid)

    if chosen_slot == "0":
        return "0"  # New game option selected
    else:
        return slots[int(chosen_slot) - 1].lstrip("slot")  # Convert to zero-based index

def list_saves(saves, starting_string: str = "Available Save Slots:"):
    strings = [starting_string, "0 = Back"]
    valid = ["0"]

    

    for i in range(1, 6):
        slot_name = f"slot{i}"
        if slot_name not in saves:
            strings.append(f"{i} = Empty Slot")
            valid.append(str(i))
        else:
            name = saves[slot_name]['player']
            style = saves[slot_name]['class']
            level = saves[slot_name]['level']
            dungeon = saves[slot_name]['dungeon']
            strings.append(f"{i} = {slot_name} [{name} - {style}, Level: {level}, Dungeon: {dungeon}]")
            valid.append(str(i))
            

    return "\n".join(strings), valid

def status_menu(player: Player):
    stats = [player.strength, player.agility, player.constitution, player.wisdom, player.luck]
    
    print(divider)
    print(f"Name: {player.name}")
    print(f"Class: {player.style}")
    print(f"Level: {player.level}")
    print(f"Experience to next level: {player.exp}")
    print(f"Stats:\nStrength: {stats[0]}, Agility: {stats[1]}, Constitution: {stats[2]}, Wisdom: {stats[3]}, Luck: {stats[4]}")
    print(f"Health: {player.health}/{player.max_health}")
    print(f"Mana: {player.mana}/{player.max_mana}")
    print(f"Armor: {player.armor}, Magic Resist: {player.magic_resist}")
    print(f"Physical Damage: {player.phys_damage}, Magical Damage: {player.mage_damage}")
    print(f"Skills: {player.skills}")
    print(f"Spells: {player.spells}")
    print(f"Equipment:\nHead: {player.head_armor}\nBody: {player.body_armor}\nWeapon: {player.weapon}")

def main_save_menu(player: Player, shop: Shop, dungeon: Dungeon):
    prompt = "Manage Saved Games:\n0 = Back\n1 = Save Game\n2 = Delete Save"
    
    while True:
        choice = validate_input(prompt, ["0", "1", "2"])
        saves = list_saves_summary()
        match choice:
            case "0":
                return True
            case "1":  # Save Game
                prompt, valid = list_saves(saves)
                save_slot = validate_input(prompt, valid)
                if save_slot != "0":
                    save_game(player, shop, dungeon, int(save_slot)) # type: ignore
                    return True
            case "2": # Delete Save
                prompt, valid = list_saves(saves, "Choose Slot to Delete:")
                delete_slot = validate_input(prompt, valid)
                delete_slot = "slot" + delete_slot

                if delete_slot in saves:
                    delete_save(delete_slot)
                    return True
                    

        