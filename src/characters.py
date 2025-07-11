from equipment import *
from Constants import *
from item import Item

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
        self.lifesteal = 0  # Default lifesteal value

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
        self.invent = []
        
    def take_damage(self, damage, dmg_type):
        # Pretty self explanatory, takes damage based on damage type and armor
        #print(f"Incoming damage: {damage}. Armor: {self.armor}, MR: {self.magic_resist}")
        actual_dmg = 0
        if dmg_type == "physical":
            actual_dmg = max(1, damage - (self.armor * 5))
            self.health = self.health - actual_dmg
            print(f"{self.name} takes {actual_dmg} physical damage.")
        elif dmg_type == "magical":
            actual_dmg = max(1, damage - (self.magic_resist * 5))
            self.health = self.health - actual_dmg
            print(f"{self.name} takes {actual_dmg} magical damage.")
        elif dmg_type == "true":
            actual_dmg = damage  # True damage ignores armor and magic resist
            self.health = self.health - actual_dmg
            print(f"{self.name} takes {actual_dmg} true damage.")
        
        if self.health > 0:
            print(f"{self.name} has {self.health} health remaining.")
        else:
            print(f"{self.name} has died.")
        
        return actual_dmg

    def __str__(self):
        # For debugging character creation
        return f"""Name: {self.name}, Strength: {self.strength}, Agility: {self.agility}, \
Constitution: {self.constitution}, Wisdom: {self.wisdom}, Luck: {self.luck},\nHead Slot: {self.head_armor.name}, \
Body Slot: {self.body_armor.name}, Weapon: {self.weapon.name},\nArmor: {self.armor}, Magic Resist: {self.magic_resist}"""
    
    def equip_item(self, equipment: Equipment):
        # equipment class must be used.
        slot = equipment.slot
        armor = equipment.armor
        mr = equipment.mr
        p_dmg = equipment.phys_damage
        m_dmg = equipment.mage_damage
        ls = equipment.lifesteal

        print(f"Equipping {equipment.name} to {self.name}")

        if slot == "head":
            old_equip = self.head_armor
            self.head_armor = equipment
        elif slot == "body":
            old_equip = self.body_armor
            self.body_armor = equipment
        elif slot == "weapon":
            old_equip = self.weapon
            self.weapon = equipment
        else:
            raise ValueError("Invalid equipment")
        
        self.armor += armor
        self.magic_resist += mr
        self.phys_damage += p_dmg
        self.mage_damage += m_dmg
        self.lifesteal += ls
        
        if not (old_equip.name == "None" or old_equip.name == "Plain Clothes" or old_equip.name == "Fist"):
            self.armor -= old_equip.armor
            self.magic_resist -= old_equip.mr
            self.phys_damage -= old_equip.phys_damage
            self.mage_damage -= old_equip.mage_damage
            if hasattr(old_equip, "lifesteal"):
                self.lifesteal -= old_equip.lifesteal
            temp = Item(old_equip)
            self.invent.append(temp)
        
        if "Lucky" in equipment.name:
            self.luck += 2

        if "Lucky" in old_equip.name:
            self.luck -= 2
    
    def melee_strike(self, target):
        # Calculating melee damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} strikes {target.name}.")
        actual_dmg = target.take_damage(dmg, "physical")
        if hasattr(self, "lifesteal") and self.lifesteal > 0:
            heal_amount = round(self.lifesteal/100 * actual_dmg)
            print(f"{self.name} heals for {heal_amount} health.")
            self.health = min(self.max_health, self.health + heal_amount)

    def get_class_type(self):
        return type(self).__name__

def get_starting_stats(points=45):
    stats = ["str", "agi", "con", "wis", "luck"]
    strength = 1
    agility = 1
    constitution = 1
    wisdom = 1
    luck = 1
    
    stat_list = random.choices(stats, k=points)

    for item in stat_list:
        if item == "str":
            strength += 1
        elif item == "agi":
            agility += 1
        elif item == "con":
            constitution += 1
        elif item == "wis":
            wisdom += 1
        elif item == "luck":
            luck += 1
    
    return [strength, agility, constitution, wisdom, luck]