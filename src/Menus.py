import random
from characters import Character
from random_functions import *

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

def skills_menu(player: Character,enemies: list):
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

def spells_menu(player: Character,enemies: list):
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

def main_combat_menu(player: Character, enemies: list):
    while True:
        prompt = ("1 = Basic Attack\n2 = Skills\n3 = Spells\n4 = Flee")
        valid_inputs = ["1", "2", "3", "4"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "1": #Basic Attack - might need to check if player == archer and if so use basic_shot rather than melee_strike
                target_str = target_selection_menu(enemies)
                if target_str != "0":
                    target = enemies[int(target_str)-1]
                    if player.sytle == "Archer":
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
            
def main_menu(player: Character):
    while True:
        prompt = ("1 = Explore Dungeon\n2 = Inventory\n3 = Shop\n4 = Exit")
        valid_inputs = ["1", "2", "3", "4"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "1":
                #Need some dungeon menu to call here
                return True
            case "2":
                print(f"Inventory: {player.invent}")
                print(divider)
                prompt = ["Choose item:", "0 = Back"]
                valid_inputs = ["0"]
                keys_list = list(player.invent.keys())
                
                for i in range(len(player.invent)):
                    prompt.append(f"{i+1} = {keys_list[i]}")
                    valid_inputs.append(f"{i+1}")

                choice = int(validate_input("\n".join(prompt), valid_inputs))
                item_key = keys_list[choice - 1]

                use_item_menu(player, item_key)
                return True

            case "3":
                shop_menu(player)
                return True
            case "4":
                return False

def shop_menu(player: Character):
    pass

def use_item_menu(player: Character, item_key):
    if isinstance(player.invent[item_key], Equipment):
        item = player.invent[item_key]

        slot = item.slot # type: ignore

        match slot:
            case "head":
                player.head_armor.compare_equipment(item)
            case "body":
                player.body_armor.compare_equipment(item)
            case "weapon":
                player.weapon.compare_equipment(item)

        prompt = "Would you like to equip this item?\n1 = Yes\n2 = No"
        choice = validate_input(prompt, ["1", "2"])

        if choice == "2":
            return
        else:
            player.equip_item(item) # type: ignore

    else:
        item = item_key
        quantity = player.invent[item_key]

        if item == "HEALTH POTION(S)":
            #use the health potion (y/n)
            pass
        elif item == "MANA POTION(S)":
            #use the mana potion (y/n)
            pass
        elif "SPELLBOOK" in item:
            #use the spell book (y/n)
            pass
        elif "SKILLBOOK" in item:
            #use the skill book (y/n)
            pass
        elif item == "COINS":
            print("Lovely money!")
            return