import random
from characters import *
from archer import *
from Warrior import *
from Mage import *
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
                    if enemies[int(target_str) - 1]:
                        target2 = enemies[int(target_str) - 1]
                    else:
                        target2 = None
                    if enemies[int(target_str) + 1]:
                        target3 = enemies[int(target_str) + 1]
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
                target = enemies[int(target_str)]
                spell_str = "cast_" + player.spells[int(choice) - 1].lower().replace(" ", "_")

                if spell_str in splash_spells:
                    if enemies[int(target_str) - 1]:
                        target2 = enemies[int(target_str) - 1]
                    else:
                        target2 = None
                    if enemies[int(target_str) + 1]:
                        target3 = enemies[int(target_str) + 1]
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
        prompt = ("1. Basic Attack\n2. Skills\n3. Spells\n4. Flee")
        valid_inputs = ["1", "2", "3", "4"]
        choice = validate_input(prompt, valid_inputs)

        match choice:
            case "1":
                target_str = target_selection_menu(enemies)
                if target_str != "0":
                    target = enemies[int(target_str)]
                    player.melee_strike(target)
                    return
                
            case "2":
                action_taken = skills_menu(player, enemies)
                if action_taken:
                    return
                
            case "3":
                action_taken = spells_menu(player, enemies)
                if action_taken:
                    return
            
            case "4":
                return