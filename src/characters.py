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
                       "HEALTH POTIONS": 0,
                       "MANA POTIONS": 0
                       }

    def take_damage(self, damage, dmg_type):
        # Pretty self explanatory, takes damage based on damage type and armor
        print(f"Incoming damage: {damage}. Armor: {self.armor}, MR: {self.magic_resist}")
        if dmg_type == "physical":
            self.health = self.health - max(0, damage - (self.armor * 5))
            print(f"{self.name} takes {max(0, damage - (5 * self.armor))} physical damage.")
        elif dmg_type == "magical":
            self.health = self.health - max(0, damage - (self.magic_resist * 5))
            print(f"{self.name} takes {max(0, damage - (self.magic_resist * 5))} magical damage.")
        elif dmg_type == "true":
            self.health = self.health - max(0, damage)
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
    
    def melee_strike(self, target):
        # Calculating melee damage
        dmg = max(1, self.phys_damage + (5 * self.strength))
        print(f"{self.name} strikes {target.name} for {dmg} physical damage.")
        target.take_damage(dmg, "physical")

    def get_class_type(self):
        return type(self).__name__

class Enemy(Character):
    def __init__(self, name, stats, diff_modifier = 1.0):
        #increase base stats by difficulty modifier
        new_stats = stats.copy()
        for stat in new_stats:
            stat = stat * diff_modifier
        super().__init__(name, new_stats)
