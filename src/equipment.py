import random

class Equipment():
    def __init__(self, name, slot, armor, mr, damage):
        self.name = name
        self.slot = slot
        self.armor = armor
        self.mr = mr
        self.damage = damage
    
    def __str__(self) -> str:
        return f"{self.name}:\n\
            Slot: {self.slot}\n\
            Armor: {self.armor}\n\
            Magic Resist: {self.mr}\n\
            Damage: {self.damage}"