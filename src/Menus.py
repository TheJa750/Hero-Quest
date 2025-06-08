import random, time
from player import Player
from dungeon import Dungeon, Room
from equipment import create_new_equipment, Equipment
from Constants import *
from Enemy import Enemy
from shop import Shop
from item import Item

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
        prompt = ("1 = Explore Dungeon\n2 = Inventory\n3 = Shop\n4 = Exit")
        valid_inputs = ["1", "2", "3", "4"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "1":
                return dungeon_menu(player, current_dungeon, current_shop)
            case "2":
                print(f"Inventory: {player.invent}")
                print(divider)
                prompt = ["Choose item:", "0 = Back"]
                valid_inputs = ["0"]
                
                for i in range(len(player.invent)):
                    prompt.append(f"{i+1} = {player.invent[i]}")
                    valid_inputs.append(f"{i+1}")

                choice = int(validate_input("\n".join(prompt), valid_inputs))
                item = player.invent[choice - 1]

                use_item_menu(player, item)
                return True
            case "3":
                shop_menu(player, current_shop)
                return True
            case "4":
                return False

def shop_menu(player: Player, shop: Shop):
    print("Welcome to the Fantasy Shop!")
    print("Can I interest you in any of our fine wares?")
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
                shop.sell_item()
            case _:
                shop.buy_item(choice-2)
        
        if not user_yes_no_check("shopping", "continue"):
            return
    
def use_item_menu(player:Player, item: Item):
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
        else:
            return
        
    else:
        match item.name:
            case "HEALTH POTION":
                if item.quantity > 0:
                    if user_yes_no_check(item.name, "use"):
                        item.quantity -= 1
                        player.health = player.max_health
                        print("Drinking health potion...")
                        print(f"Health recovered! {player.name} now has {player.health} health.")
            case "MANA POTION":
                if item.quantity > 0:
                    if user_yes_no_check(item, "use"):
                        item.quantity -= 1
                        player.mana = player.max_mana
                        print("Drinking mana potion...")
                        print(f"Mana recovered! {player.name} now has {player.mana} mana.")
            case "SPELLBOOK":
                spell_list = spells.copy()
                if item.quantity > 0:
                    if user_yes_no_check(item, "use"):
                        item.quantity -= 1
                        for spell in player.spells:
                            spell_list.remove(spell) 
                        new_spell = random.choice(spell_list)
                        player.learn_spell(new_spell)
            case "SKILLBOOK":
                skill_list = skills.copy()
                if item.quantity > 0:
                    if user_yes_no_check(item, "use"):
                        item.quantity -= 1
                        for skill in player.skills:
                            skill_list.remove(skill)
                        if player.style != "Archer":
                            skill_list.remove("Double Shot")
                            skill_list.remove("Piercing Shot")
                        new_skill = random.choice(skill_list)
                        player.learn_skill(new_skill)
            case "COINS":
                print("Lovely money!")
            case _:
                print("I wonder what I can do with this... Maybe I can sell it?")
        
        return
        
def user_yes_no_check(item, function: str):
    prompt = f"Would you like to {function} {item}?\n1 = Yes\n2 = No"
    choice = validate_input(prompt, ["1", "2"])

    if choice == "1":
        return True
    else:
        return False
    
def dungeon_menu(player: Player, dungeon: Dungeon, shop: Shop):
    print(dungeon)

    if not user_yes_no_check(dungeon.name, "explore"):
        return True
    
    keep_exploring = True

    while keep_exploring:
        room = dungeon.next_room() #type: Room | str
        print(divider)
        

        if isinstance(room, str): #Only type str when dungeon complete, returns to main menu to begin new loop
            print(room)
            shop.restock_items()
            return True
        
        print(repr(room))
        action_code = battle(player, room.enemies)

        match action_code:
            case 0:
                pass
            case 1: #Flee, return room to dungeon -> floor 0 -> room 0 then return to main menu with True (continue playing)
                dungeon.floors[0].rooms.insert(0, room)
                return True
            case 2: #player has died return to main menu with False (stop playing)
                player.death()
                return False
        
        keep_exploring = user_yes_no_check(dungeon.name, "explore")

    return True
            
def battle(player: Player, enemies: list[Enemy]):
    #Need some logic determining battle order, for now player will always go first so that I can make the battle loop work
    
    #Main battle loop, if player is alive and at least 1 enemy is alive battle continues
    while player.health > 0 and len(enemies) > 0:


        action_code = main_combat_menu(player, enemies)
        print(divider)

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
                time.sleep(0.25)
                enemy.melee_strike(player)
                print(divider)
                if player.health <= 0:
                    return 2

    return 0
