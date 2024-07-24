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
        self.__strength = stats[0]
        self.__agility = stats[1]
        self.__constitution = stats[2]
        self.__wisdom = stats[3]
        self.__luck = stats[4]

        # Calculating Health/Mana based on stats:
        self.health = 100 * self.__constitution
        self.mana = 25 * self.__wisdom
        self.armor = 0
        self.magic_resist = 0
        self.damage = 1

        # Creating list of skills & spells:
        self.skills = []
        self.spells = []

        # Creating equipment slots:
        self.head_armor = []
        self.body_armor = []
        self.weapon = []

        starting_gear_head = Equipment("None", equipment_slot_head, 0, 0, 0)
        starting_gear_body = Equipment("Plain Clothes", equipment_slot_body, 1, 1, 0)
        starting_gear_weapon = Equipment("Fist", equipment_slot_wep, 0, 0, 5)

        self.equip_item(starting_gear_head)
        self.equip_item(starting_gear_body)
        self.equip_item(starting_gear_weapon)

        # Creating starting invetory shared by all types:
        self.invent = {"COINS": 100,
                       "HEALTH POTIONS": 0,
                       }



    def take_damage(self, damage, dmg_type):
        # Pretty self explanatory, takes damage based on damage type and armor
        if dmg_type == "physical":
            self.health = self.health - max(0, damage - (self.armor * 5))
        if dmg_type == "magical":
            self.health = self.health - max(0, damage - (self.magic_resist * 5))

    def __str__(self):
        # For debugging character creation
        return f"""Name: {self.name}, Strength: {self.__strength}, Agility: {self.__agility},\
             Constitution: {self.__constitution}, Wisdom: {self.__wisdom}, Luck: {self.__luck}"""
    
    def equip_item(self, equipment: Equipment):
        # equipment class must be used.
        slot = equipment.slot
        armor = equipment.armor
        mr = equipment.mr
        dmg = equipment.damage

        print(f"Equipping {equipment.name} to {self.name}")

        if slot == "head":
            old_equip = self.head_armor
            if old_equip != []:
                self.armor -= old_equip.armor
                self.magic_resist -= old_equip.mr
                self.damage -= old_equip.damage
            self.head_armor = equipment
        if slot == "body":
            old_equip = self.body_armor
            if old_equip != []:
                self.armor -= old_equip.armor
                self.magic_resist -= old_equip.mr
                self.damage -= old_equip.damage
            self.body_armor = equipment
        if slot == "weapon":
            old_equip = self.weapon
            if old_equip != []:
                self.armor -= old_equip.armor
                self.magic_resist -= old_equip.mr
                self.damage -= old_equip.damage
            self.weapon = equipment
        raise ValueError("Invalid equipment")
    
    def melee_strike(self, target):
        # Calculating melee damage
        print(f"{self.name} strikes {target.name} for {max(0, self.damage - (target.armor * 5))} physical damage.")
        target.take_damage(self.damage, "physical")

class Mage(Character):
    def __init__(self, name, stats, spells):
        super().__init__(name, stats)
        for spell in spells:
            self.spells.append(spell)
        
    def cast_fireball(self, target, mana_cost):
        print(f"{self.name} attempts to cast a fireball at {target.name}.")
        base_dmg = 50
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = base_dmg + (self.__wisdom * 5)
            target.take_damage(damage, "magical")
        else:
            print(f"{self.name} has insufficient mana to cast fireball.")
        

class Archer(Character):
    def __init__(self, name, stats, skills):
        super().__init__(name, stats)
        for skill in skills:
            self.skills.append(skill)
        self.inventory = {}

    def double_shot(self, target):
        # Fires 2 arrows back to back, the second one has a 70% chance to hit for 75% of base damage
        print(f"{self.name} uses Double Shot to attack {target.name}.")
        hit_chance = random.randrange(0, 100)
        if hit_chance >= 30:
            pass

class Warrior(Character):
    def __init__(self, name, stats, skills):
        super().__init__(name, stats)
        for skill in skills:
            self.skills.append(skill)
