import random
from equipment import *
from random_functions import *

spells = ["Fireball", "Chain Lightning", "Shadow Fangs"]
skills = ["Double Shot", "Piercing Shot", "Cleave", "Devastating Blow", "Fury of Blows"]

class Character():
    def __init__(self, name, stats, style = "Monster", skills = [], spells = []):
        # Creates a character object given a name and a list of stats
        # List MUST be in the following order:
        # [Strength, Agility, Constitution, Wisdom, Luck]
        self.name = name
        self.style = style
        self.strength = stats[0]
        self.agility = stats[1]
        self.constitution = stats[2]
        self.wisdom = stats[3]
        self.luck = stats[4]
        self.exp = 100
        self.level = 1

        # Calculating Health/Mana based on stats:
        self.max_health = 100 * self.constitution
        self.health = self.max_health
        self.max_mana = 25 * self.wisdom
        self.mana = self.max_mana
        self.armor = 0
        self.magic_resist = 0
        self.phys_damage = 5 * self.strength
        self.mage_damage = 0

        # Creating list of skills & spells:
        self.skills = []
        self.spells = []

        # Creating equipment slots:
        starting_gear_head = Equipment("None", equipment_slot_head, 0, 0, 0, 0)
        starting_gear_body = Equipment("Plain Clothes", equipment_slot_body, 1, 1, 0, 0)
        starting_gear_weapon = Equipment("Fist", equipment_slot_wep, 0, 0, 5, 0)
                
        self.head_armor = starting_gear_head
        self.body_armor = starting_gear_body
        self.weapon = starting_gear_weapon

        self.armor += self.head_armor.armor + self.body_armor.armor + self.weapon.armor
        self.magic_resist += self.head_armor.mr + self.body_armor.mr + self.weapon.mr
        self.phys_damage += self.head_armor.phys_damage + self.body_armor.phys_damage + self.weapon.phys_damage
        self.mage_damage += self.head_armor.mage_damage + self.body_armor.mage_damage + self.weapon.mage_damage

        # Creating starting invetory shared by all types:
        self.invent = {"COINS": 100,
                       "HEALTH POTION(S)": 0,
                       "MANA POTION(S)": 0
                       }
        
        match self.style:
            case "Archer":
                for skill in skills:
                    self.skills.append(skill)

                self.invent["ARROWS"] = 500

                starting_gear = [Equipment("Starter's Bow", equipment_slot_wep, 0, 0, 15, 0),
                                ]
                
                for gear in starting_gear:
                    self.equip_item(gear)

            case "Mage":
                for spell in spells:
                    self.spells.append(spell)

                starting_gear = [Equipment("Starter's Wand", equipment_slot_wep, 0, 2, 5, 10),
                                Equipment("Dusty Hat", equipment_slot_head, 1, 2, 0, 1)]
                
                for gear in starting_gear:
                    self.equip_item(gear)

            case "Warrior":
                for skill in skills:
                    self.skills.append(skill)

                starting_gear = [Equipment("Starter's Sword", equipment_slot_wep, 1, -1, 10, 0),
                                Equipment("Loose Chainmail", equipment_slot_body, 3, 0, 0, 0)]
                
                for gear in starting_gear:
                    self.equip_item(gear)
            case "Monster":
                return

    def take_damage(self, damage, dmg_type):
        # Pretty self explanatory, takes damage based on damage type and armor
        #print(f"Incoming damage: {damage}. Armor: {self.armor}, MR: {self.magic_resist}")
        if dmg_type == "physical":
            self.health = self.health - max(1, damage - (self.armor * 5))
            print(f"{self.name} takes {max(1, damage - (5 * self.armor))} physical damage.")
        elif dmg_type == "magical":
            self.health = self.health - max(1, damage - (self.magic_resist * 5))
            print(f"{self.name} takes {max(1, damage - (self.magic_resist * 5))} magical damage.")
        elif dmg_type == "true":
            self.health = self.health - damage
            print(f"{self.name} takes {damage} true damage.")
        
        if self.health > 0:
            print(f"{self.name} has {self.health} health remaining.")
        else:
            print(f"{self.name} has died.")

    def __str__(self):
        # For debugging character creation
        return f"""Name: {self.name}, Strength: {self.strength}, Agility: {self.agility}, \
Constitution: {self.constitution}, Wisdom: {self.wisdom}, Luck: {self.luck},\nHead Slot: {self.head_armor.name}, \
Body Slot: {self.body_armor.name}, Weapon: {self.weapon.name},\nArmor: {self.armor}, Magic Resist: {self.magic_resist} \
\nSkills: {self.skills}, Spells: {self.spells}"""
    
    def equip_item(self, equipment: Equipment):
        # equipment class must be used.
        slot = equipment.slot
        armor = equipment.armor
        mr = equipment.mr
        p_dmg = equipment.phys_damage
        m_dmg = equipment.mage_damage

        print(f"Equipping {equipment.name} to {self.name}")

        if slot == "head":
            old_equip = self.head_armor
            self.head_armor = equipment
            self.armor += armor
            self.magic_resist += mr
            self.phys_damage += p_dmg
            self.mage_damage += m_dmg
        elif slot == "body":
            old_equip = self.body_armor
            self.body_armor = equipment
            self.armor += armor
            self.magic_resist += mr
            self.phys_damage += p_dmg
            self.mage_damage += m_dmg
        elif slot == "weapon":
            old_equip = self.weapon
            self.weapon = equipment
            self.armor += armor
            self.magic_resist += mr
            self.phys_damage += p_dmg
            self.mage_damage += m_dmg
        else:
            raise ValueError("Invalid equipment")
        
        if not (old_equip.name == "None" or old_equip.name == "Plain Clothes" or old_equip.name == "Fist"):
            self.armor -= old_equip.armor
            self.magic_resist -= old_equip.mr
            self.phys_damage -= old_equip.phys_damage
            self.mage_damage -= old_equip.mage_damage
            temp_dict = {old_equip.name: old_equip}
            self.invent.update(temp_dict)

        if equipment.name in self.invent.keys():
            self.invent.pop(equipment.name)
    
    def melee_strike(self, target):
        # Calculating melee damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} strikes {target.name}.")
        target.take_damage(dmg, "physical")

    def get_class_type(self):
        return type(self).__name__
    
    def gain_exp(self, exp_amount):
        #exp will be amount needed to reach next level.
        if exp_amount >= self.exp:
            exp = exp_amount - self.exp #get remainder toward next level
            self.level_up() #level up and calc new exp requirement
            self.exp -= exp #remove remainder from new requirement
        else:
            self.exp -= exp_amount #count down toward leveling up

        print(f"Exp remaining until level {self.level + 1}: {self.exp}")

    def level_up(self):
        self.level += 1
        exp_needed = 0
        for i in range(self.level + 1):
            exp_needed += i * 100
        self.exp = exp_needed
        print(f"Congratulations! {self.name} has reached level {self.level}!")
        print(divider)
        
        if self.level % 5 == 0:
            self.add_stats(6) #double points every 5th level
        else:
            self.add_stats(3)

        #Refill health/mana and update physical damage
        self.max_health = 100 * self.constitution
        self.health = self.max_health
        self.max_mana = 25 * self.wisdom
        self.mana = self.max_mana
        self.phys_damage = ((5 * self.strength) + self.head_armor.phys_damage
                            + self.body_armor.phys_damage + self.weapon.phys_damage)

    def add_stats(self, new_points):
        print(f"{new_points} stat point(s) available.")
        print("How would you like to distribute these point(s)?") # [Strength, Agility, Constitution, Wisdom, Luck]
        valid_inputs = ["1", "2", "3", "4", "5"]
        choice = validate_input("1 = Strength\n2 = Agility\n3 = Constitution\n4 = Wisdom\n5 = Luck",
                                valid_inputs,
                                "Please select a valid stat.")
        match choice:
            case "1":
                stat = "Strength"
            case "2":
                stat = "Agility"
            case "3":
                stat = "Constitution"
            case "4":
                stat = "Wisdom"
            case _:
                stat = "Luck"
        
        valid_inputs = []
        for i in range(new_points + 1):
            valid_inputs.append(f"{i}")
        assign = validate_input(f"How many points would you like to add to {stat}?",
                                valid_inputs,
                                f"Please enter a valid amount (0 - {new_points}).")
        
        match stat:
            case "Strength":
                self.strength += int(assign)
                print(f"Strength: {self.strength}")
            case "Agility":
                self.agility += int(assign)
                print(f"Agility: {self.agility}")
            case "Constitution":
                self.constitution += int(assign)
                print(f"Constitution: {self.constitution}")
            case "Wisdom":
                self.wisdom += int(assign)
                print(f"Wisdom: {self.wisdom}")
            case "Luck":
                self.luck += int(assign)
                print(f"Luck: {self.luck}")

        if int(assign) < new_points:
            self.add_stats(new_points - int(assign))
        else:
            return
        
    def learn_skill(self, skill: str):
        self.skills.append(skill)

    def learn_spell(self, spell: str):
        self.spells.append(spell)

    def cleave(self, target1, target2 = None, target3 = None):
        #Targets up to 3 enemies target1 is main target and gets full damage, target2/3 get 75% damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} cleaves {target1.name}.")
        target1.take_damage(dmg, "physical")

        if target2 and target3:
            print(f"The sweep hits {target2.name} and {target3.name}.")
            target2.take_damage(round(0.75 * dmg), "physical")
            target3.take_damage(round(0.75 * dmg), "physical")
        elif target2:
            print(f"The sweep hits {target2.name}.")
            target2.take_damage(round(0.75 * dmg), "physical")
        elif target3:
            print(f"The sweep hits {target3.name}.")
            target3.take_damage(round(0.75 * dmg), "physical")
        else:
            print("No other targets in range.")

        return True

    def devastating_strike(self, target):
        #Deals true damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} lands a powerful blow on {target.name}.")
        target.take_damage(dmg, "true")

        return True

    def fury_of_blows(self, target):
        #Attacks a random number of times (2-5 inclusive), each for 50% damage
        num_attacks = random.randint(2,5)
        dmg = max(1, 0.5 * self.phys_damage)
        print(f"{self.name} quickly attacks {target.name} {num_attacks} times.")
        for i in range(0, num_attacks):
            target.take_damage(round(dmg), "physical")
        return True

    def basic_shot(self, target,dmg_mod = 1.0, dmg_type = "physical"):
        if self.invent['ARROWS'] > 0:
            print(f"{self.name} shoots {target.name}.")
            self.invent['ARROWS'] -= 1
            target.take_damage(round(dmg_mod * self.phys_damage), dmg_type)
            print(f"Arrows remaining: {self.invent['ARROWS']}.")
        else:
            print("Not enough arrows!")
            self.melee_strike(target)

    def double_shot(self, target):
        # Fires 2 arrows back to back, the second one has a 70% chance to hit for 75% of base damage
        print(f"{self.name} uses Double Shot to attack {target.name}.")
        self.basic_shot(target)
        hit_chance = random.randint(0, 100)
        if hit_chance >= 30:
            self.basic_shot(target, 0.75)
        else:
            print(f"{self.name}'s 2nd shot misses.")
        return True

    def piercing_shot(self, target):
        #Fires a shot that ignores armor
        print(f"{self.name} uses Piercing Shot to attack {target.name}.")
        self.basic_shot(target, dmg_type="true")
        return True

    def cast_fireball(self, target):
        print(f"{self.name} attempts to cast Fireball at {target.name}.")
        base_dmg = 50
        mana_cost = 25
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = round(base_dmg + (self.wisdom * 5) + self.mage_damage)
            print(f"Fireball hits {target.name}.")
            target.take_damage(damage, "magical")
            
            return True
        else:
            print(f"{self.name} has insufficient mana to cast Fireball.")
            return False
    
    def cast_chain_lightning(self, target1, target2 = None, target3 = None):
        #Lightning spell that chains to nearby enemies
        print(f"{self.name} attempts to cast Chain Lightning at {target1.name}.")
        base_dmg = 30
        mana_cost = 30
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            dmg = round(base_dmg + (self.wisdom * 2.5) + self.mage_damage)
            print(f"Chain Lightning hits {target1.name}.")
            target1.take_damage(dmg, "magical")
            
            if target2 and target3:
                print(f"The lightning arcs to {target2.name} and {target3.name}.")
                target2.take_damage(dmg, "magical")
                target3.take_damage(dmg, "magical")
            elif target2:
                print(f"The lightning arcs to {target2.name}.")
                target2.take_damage(dmg, "magical")
            elif target3:
                print(f"The lightning arcs to {target3.name}.")
                target3.take_damage(dmg, "magical")
            else:
                print("No other targets in range.")

            return True
        else:
            print(f"{self.name} has insufficient mana to cast Chain Lightning.")
            return False
        
    def cast_shadow_fangs(self, target):
        # Shadow Fangs - strikes target twice, each one gets offensive bonuses to damage, but also defensive reduction to damage.
        print(f"{self.name} attempts to cast Shadow Fangs at {target.name}.")
        base_dmg = 20
        mana_cost = 20
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = round(base_dmg + (self.wisdom * 2.5) + self.mage_damage)
            print(f"Shadow Fangs hits {target.name}.")
            target.take_damage(damage, "magical")
            print(f"Shadow Fangs hits {target.name}.")
            target.take_damage(damage, "magical")
            return True
        else:
            print(f"{self.name} has insufficient mana to cast Shadow Fangs.")
            return False

class Enemy(Character):
    def __init__(self, name, stats, level = 1, growth = 1, base_exp = 20):
        #level is for scaling monsters, growth is for stat points per level (in each stat)
        super().__init__(name, stats)
        self.growth = growth

        if level > 1:
            for i in range(self.level, level + 1):
                self.level_up_enemy()

        self.exp = (base_exp * 2 * growth) + (self.level * base_exp)

    def __str__(self):
        return f"Name: {self.name} Level: {self.level} Health: {self.health}"
    
    def level_up_enemy(self):
        self.level += 1
               
        self.add_enemy_stats(self.growth)

        #Refill health/mana and update physical damage
        self.max_health = 100 * self.constitution
        self.health = self.max_health
        self.max_mana = 25 * self.wisdom
        self.mana = self.max_mana
        self.phys_damage = ((5 * self.strength) + self.head_armor.phys_damage
                            + self.body_armor.phys_damage + self.weapon.phys_damage)
        
    def add_enemy_stats(self, per_level):
        self.strength += per_level
        self.agility += per_level
        self.constitution += per_level
        self.wisdom += per_level
        self.luck += per_level

    def give_exp(self, player: Character):
        player.gain_exp(self.exp)