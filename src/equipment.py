import random

class Equipment():
    def __init__(self, name, slot, armor, mr, melee_damage, mage_dmg):
        self.name = name
        self.slot = slot
        self.armor = armor
        self.mr = mr
        self.phys_damage = melee_damage
        self.mage_damage = mage_dmg
    
    def __str__(self) -> str:
        return f"{self.name}:\n\
            Slot: {self.slot}\n\
            Armor: {self.armor}\n\
            Magic Resist: {self.mr}\n\
            Physical Damage: {self.phys_damage}\n\
            Magical Damage: {self.mage_damage}"
    
def create_new_equipment(player, game_stage):
    pass