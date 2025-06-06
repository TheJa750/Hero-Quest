import random
from characters import Character, skills, spells
from random_functions import *
from equipment import create_new_equipment, Equipment

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
    print("Welcome to the Fantasy Shop!")
    print("Can I interest you in any of our fine wares?")

    num_equip = random.randint(int(round(player.luck/7)), int(round(player.luck)/3))
    
    items = [
        "HEALTH POTION(S)",
        "MANA POTION(S)"
    ]

    prices = {
        "HEALTH POTION(S)": 50,
        "MANA POTION(S)": 50
    }

    equip = []

    for i in range(num_equip):
        item = create_new_equipment(player)
        items.append(item.name)
        price = (5 * (item.armor + item.mr)) + (2 * (item.phys_damage + item.mage_damage))
        prices[item.name] = price
        equip.append(item)

    prompt = ["0 = Back"]
    valid = ["0"]

    for i in range(len(items)):
        prompt.append(f"{i+1} = {items[i]}")
        valid.append(f"{i+1}")

    choice = items[int(validate_input("\n".join(prompt), valid)) - 1]
    equip_names = []

    for i in range(len(equip)):
        equip_names.append(equip[i].name)

    cost = prices[choice]
    money = player.invent["COINS"]

    while True:
        if choice in equip_names:
            index = equip_names.index(choice)
            comp = equip[index]
            slot = comp.slot
            if slot == "head":
                player.head_armor.compare_equipment(comp)
            elif slot == "body":
                player.body_armor.compare_equipment(comp)
            else:
                player.weapon.compare_equipment(comp)
            print(f"{comp.name} will cost {cost} coins.")
            if user_yes_no_check(comp.name, "buy"):
                break
            else:
                return
        else:
            break

    if money < cost:
        print("Insufficient funds, please come back richer.")
        return
    
    player.invent["COINS"] -= cost
    
    if not (choice in equip_names):
        if choice in player.invent.keys():
            player.invent[choice] += 1
        else:
            player.invent[choice] = 1
    else:
        index = equip_names.index(choice)
        player.invent[choice] = equip[index]

    print(f"{player.name} pays {cost} coins to the cashier.")
    print(f"{choice} has been added to inventory.")
    return

def use_item_menu(player: Character, item_key):
    item = player.invent[item_key]
    if isinstance(item, Equipment):
        slot = item.slot

        match slot:
            case "head":
                player.head_armor.compare_equipment(item)
            case "body":
                player.body_armor.compare_equipment(item)
            case "weapon":
                player.weapon.compare_equipment(item)

        if user_yes_no_check(item.name, "equip"): 
            player.equip_item(item)
        else:
            return

    else:
        item = item_key
        quantity = player.invent[item_key]

        if item == "HEALTH POTION(S)":
            if quantity > 0:
                if user_yes_no_check(item, "use"):
                    player.invent[item] -= 1
                    player.health = player.max_health
                    print("Drinking health potion...")
                    print(f"Health recovered! {player.name} now has {player.health} health.")
        elif item == "MANA POTION(S)":
            if quantity > 0:
                if user_yes_no_check(item, "use"):
                    player.invent[item] -= 1
                    player.mana = player.max_mana
                    print("Drinking mana potion...")
                    print(f"Mana recovered! {player.name} now has {player.mana} mana.")
        elif "SPELLBOOK" in item:
            spell_list = spells.copy()
            if quantity > 0:
                if user_yes_no_check(item, "use"):
                    player.invent[item] -= 1
                    for spell in player.spells:
                        spell_list.remove(spell) 
                    new_spell = random.choice(spell_list)
                    player.spells.append(new_spell)
        elif "SKILLBOOK" in item:
            skill_list = skills.copy()
            if quantity > 0:
                if user_yes_no_check(item, "use"):
                    player.invent[item] -= 1
                    for skill in player.skills:
                        skill_list.remove(skill) 
                    new_skill = random.choice(skill_list)
                    player.spells.append(new_skill)
        elif item == "COINS":
            print("Lovely money!")
        else:
            print("I wonder what I can do with this... Maybe I can sell it?")
        
        return
        
def user_yes_no_check(item, function: str):
    prompt = f"Would you like to {function} {item}?\n1 = Yes\n2 = No"
    choice = validate_input(prompt, ["1", "2"])

    if choice == "1":
        return True
    else:
        return False