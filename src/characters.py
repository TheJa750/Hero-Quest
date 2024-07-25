import random
from equipment import *

equipment_slot_head = "head"
equipment_slot_body = "body"
equipment_slot_wep = "weapon"

class Character():
    def __init__(self, name, stats):
        # Creates a character object given a name and a list of stats
        # List MUST be in the following order:
        # [Strength, Agility, Constitution, Wisdom, Luck]
        self.name = name
        self.strength = stats[0]
        self.agility = stats[1]
        self.constitution = stats[2]
        self.wisdom = stats[3]
        self.luck = stats[4]

        # Calculating Health/Mana based on stats:
        self.health = 100 * self.constitution
        self.mana = 25 * self.wisdom
        self.armor = 0
        self.magic_resist = 0
        self.phys_damage = 0
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
                       "HEALTH POTIONS": 0,
                       "MANA POTIONS": 0
                       }



    def take_damage(self, damage, dmg_type):
        # Pretty self explanatory, takes damage based on damage type and armor
        if dmg_type == "physical":
            self.health = self.health - max(0, damage - (self.armor * 5))
        if dmg_type == "magical":
            self.health = self.health - max(0, damage - (self.magic_resist * 5))

    def __str__(self):
        # For debugging character creation
        return f"""Name: {self.name}, Strength: {self.strength}, Agility: {self.agility}, \
Constitution: {self.constitution}, Wisdom: {self.wisdom}, Luck: {self.luck}"""
    
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
            self.mage_damage -+ old_equip.mage_damage
            self.invent[old_equip.name] = old_equip
    
    def melee_strike(self, target):
        # Calculating melee damage
        print(f"{self.name} strikes {target.name} for {max(0, self.damage - (target.armor * 5))} physical damage.")
        target.take_damage(self.phys_damage, "physical")

class Mage(Character):
    def __init__(self, name, stats, spells):
        super().__init__(name, stats)
        for spell in spells:
            self.spells.append(spell)

        starting_gear = [Equipment("Starter's Wand", equipment_slot_wep, 0, 2, 5, 10),
                         Equipment("Dusty Hat", equipment_slot_head, 1, 2, 0, 1)]
        
        for gear in starting_gear:
            self.equip_item(gear)
        
    def cast_fireball(self, target, mana_cost):
        print(f"{self.name} attempts to cast a fireball at {target.name}.")
        base_dmg = 50
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = base_dmg + (self.wisdom * 5)
            target.take_damage(damage, "magical")
            print(f"Fireball hits {target.name} for {max(0, damage - (target.magic_resist * 5))} magical damage.")
            if target.health > 0:
                print(f"{target.name} has {target.health} health remaining")
            elif target.health <= 0:
                print(f"{target.name} has died.")
        else:
            print(f"{self.name} has insufficient mana to cast fireball.")
        

class Archer(Character):
    def __init__(self, name, stats, skills):
        super().__init__(name, stats)
        for skill in skills:
            self.skills.append(skill)

        self.invent["ARROWS"] = 500

        starting_gear = [Equipment("Starter's Bow", equipment_slot_wep, 0, 0, 15, 0),
                         ]
        
        for gear in starting_gear:
            self.equip_item(gear)

    def double_shot(self, target):
        # Fires 2 arrows back to back, the second one has a 70% chance to hit for 75% of base damage
        print(f"{self.name} uses Double Shot to attack {target.name}.")
        hit_chance = random.randint(0, 100)
        if hit_chance >= 30:
            pass

class Warrior(Character):
    def __init__(self, name, stats, skills):
        super().__init__(name, stats)
        for skill in skills:
            self.skills.append(skill)

        starting_gear = [Equipment("Starter's Sword", equipment_slot_wep, 1, -1, 10, 0),
                         Equipment("Loose Chainmail", equipment_slot_body, 3, 0, 0, 0)]
        
        for gear in starting_gear:
            self.equip_item(gear)