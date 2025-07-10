import random
from characters import Character
from equipment import Equipment
from random_functions import validate_input
from Constants import *
from item import Item

starting_items = [
    Item("COINS", 100),
    Item("HEALTH POTION"),
    Item("MANA POTION")
]

class Player(Character):
    def __init__(self, name, stats, style, skills = [], spells = []):
        super().__init__(name, stats)
        self.style = style

        # Creating list of skills & spells:
        self.skills = []
        self.spells = []

        for item in starting_items:
            self.add_to_invent(item)

        match self.style:
            case "Archer":
                for skill in skills:
                    self.skills.append(skill)

                self.add_to_invent(Item("ARROWS", 500))

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

    def add_to_invent(self, item: Item):
        exists, index = self.check_for_item(item.name)
        if exists:
            self.invent[index].quantity += item.quantity
        else:
            self.invent.append(item)

    def check_for_item(self, item_name: str):
        exists = False
        index = -1
        for obj in self.invent:
            if obj == item_name:
                index = self.invent.index(obj)
                exists = True
        return exists, index 
    
    def get_item(self, item_name: str):
        exists, index = self.check_for_item(item_name)
        if exists:
            return self.invent[index] #type: Item

    def gain_exp(self, exp_amount):
        #exp will be amount needed to reach next level.
        if exp_amount >= self.exp:
            exp = exp_amount - self.exp #get remainder toward next level
            self.level_up() #level up and calc new exp requirement
            self.gain_exp(exp) #recursively call in cases of gaining enough xp for 2 levels at once.
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
        print(f"Str: {self.strength}, Agi: {self.agility}, Con: {self.constitution}, Wis: {self.wisdom}, Luck: {self.luck}")
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
            
        print(divider)

        if int(assign) < new_points:
            self.add_stats(new_points - int(assign))
        else:
            return
        
    def learn_skill(self, skill: str):
        print(f"{self.name} has learned {skill}.")
        self.skills.append(skill)

    def learn_spell(self, spell: str):
        print(f"{self.name} has learned {spell}.")
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
        for item in self.invent:    
            if item.name == "ARROWS":
                arrows = item #type: Item

        if arrows.quantity > 0: #type: ignore
            print(f"{self.name} shoots {target.name}.")
            arrows.quantity -= 1 #type: ignore
            target.take_damage(round(dmg_mod * self.phys_damage), dmg_type)
            print(f"Arrows remaining: {arrows.quantity}.") #type: ignore
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
        
    def cast_heal(self):
        healing = round(50 + (2.5 * self.wisdom))
        mana_cost = 50

        print(f"{self.name} attempts to cast Heal.")

        if self.mana - mana_cost >= 0:
            self.health = min(self.max_health, self.health + healing )
            return True
        else:
            print(f"{self.name} has insufficient mana to cast Heal.")
            return False
        
    def death(self):
        print("Thank you for playing Hero Quest.")