from player import Player
from dungeon import Dungeon, Room
from equipment import create_new_equipment, Equipment
from Constants import *
from Enemy import Enemy
from shop import Shop, basic_items
from item import Item

def dev_menu(player: Player, current_dungeon: Dungeon, current_shop: Shop):
    continue_menu = True
    while continue_menu:
        match input("Enter command: ").strip().lower():
            case "back":
                continue_menu = False
            case "reset_shop":
                current_shop.restock_items()
                print("Restocking shop items...")
            case "reset_dungeon":
                current_dungeon.floors.clear()  # Clear all floors in the dungeon
                print("Clearing dungeon floors...")
            case "unlearn_skill":
                strings = ["Available Skills:", "0 = Back"]
                valid = ["0"]
                for i in range(len(player.skills)):
                    strings.append(f"{i+1} = {player.skills[i]}")
                    valid.append(str(i+1))
                prompt = "\n".join(strings)
                choice = validate_input(prompt, valid)
                if choice != "0":
                    skill = player.skills[int(choice) - 1]
                    player.skills.remove(skill)
                    print(f"Unlearned skill: {skill}")
            case "unlearn_spell":
                strings = ["Available Spells:", "0 = Back"]
                valid = ["0"]
                for i in range(len(player.spells)):
                    strings.append(f"{i+1} = {player.spells[i]}")
                    valid.append(str(i+1))
                prompt = "\n".join(strings)
                choice = validate_input(prompt, valid)
                if choice != "0":
                    spell = player.spells[int(choice) - 1]
                    player.spells.remove(spell)
                    print(f"Unlearned skill: {spell}")
            case "level_up":
                exp = player.exp
                player.gain_exp(exp)
            case "add_basic_item":
                match input("Enter item name: ").strip().upper():
                    case item_name:
                        if item_name in basic_items:
                            quantity = int(input(f"Enter quantity for {item_name}: "))
                            item = Item(item_name, quantity)
                            player.add_to_invent(item)
                            print(f"Added {item_name} to inventory.")
                        else:
                            print("Item not found in basic items.")
            case "create_equipment":
                name = input("Enter equipment name: ")
                if name != "back":
                    slot = input("Enter equipment slot (head, body, weapon): ").strip().lower()
                    armor = int(input("Enter armor value: "))
                    mr = int(input("Enter magic resistance value: "))
                    phys_damage = int(input("Enter physical damage value: "))
                    mage_damage = int(input("Enter magic damage value: "))
                    ls = int(input("Enter lifesteal value (1 = 1%): "))
                    equipment = Equipment(name, slot, armor, mr, phys_damage, mage_damage, ls)
                    item = Item(equipment)
                    player.add_to_invent(item)
                    print(f"Created and added equipment: {equipment.name} to inventory.")
            case "add_money":
                amount = int(input("Enter amount of money to add: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    coins = Item("Coins", amount)
                    player.add_to_invent(coins)
                    print(f"Added {amount} coins to inventory.")
            case "add_player_attribute":
                attribute = input("Enter attribute name: ")
                value = int(input("Enter default value: "))
                setattr(player, attribute, value)
                
    return True
