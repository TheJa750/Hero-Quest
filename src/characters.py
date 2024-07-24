import random
from equipment import *

equipment_type_armor = "armor"
equipment_type_mr = "magic resist"
equipment_type_dmg = "damage"
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

        # Creating list of skills & spells:
        self.skills = []
        self.spells = []

        # Creating equipment slots:
        self.head_armor = ["None", {"type": equipment_type_armor,
                                "slot": equipment_slot_head,
                                "value": 0}]
        self.body_armor = ["Plain Clothes", {"type": equipment_type_armor,
                                "slot": equipment_slot_body,
                                "value": 1}]
        self.weapon = ["Fist", {"type": equipment_type_dmg,
                                "slot": equipment_slot_wep,
                                "value": 5}]

        # Calculating base melee damage:
        self.damage = self.__strength * 10

    def take_damage(self, damage, dmg_type):
        if dmg_type == "physical":
            self.health = self.health - max(0, damage - (self.armor * 5))
        if dmg_type == "magical":
            self.health = self.health - max(0, damage - (self.magic_resist * 5))

    def __str__(self):
        return f"""Name: {self.name}, Strength: {self.__strength}, Agility: {self.__agility},\
             Constitution: {self.__constitution}, Wisdom: {self.__wisdom}, Luck: {self.__luck}"""
    
    def equip_item(self, equipment: Equipment):
        # equipment class must be used.
        slot = equipment.slot
        value = equipment.value
        equip_type = equipment.type

        if slot == "head":
            self.head_armor = equipment
            if equip_type == equipment_type_armor:
                self.armor += value
            if equip_type == equipment_type_mr:
                self.magic_resist += value
            else:
                raise ValueError("Invalid equipment")
        if slot == "body":
            self.body_armor = equipment
            if equip_type == equipment_type_armor:
                self.armor += value
            if equip_type == equipment_type_mr:
                self.magic_resist += value
            else:
                raise ValueError("Invalid equipment")
        if slot == "weapon":
            self.weapon = equipment
            if equip_type == equipment_type_dmg:
                self.damage += value
            else:
                raise ValueError("Invalid equipment")
    
    def melee_strike(self, target):
        # Calculating melee damage
        target.take_damage(self.damage, "physical")

class Mage(Character):
    def __init__(self, name, stats):
        super().__init__(name, stats)

class Archer(Character):
    def __init__(self, name, stats):
        super().__init__(name, stats)

class Warrior(Character):
    def __init__(self, name, stats):
        super().__init__(name, stats)
