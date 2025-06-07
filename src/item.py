import random
from equipment import *
from Constants import *

prices = {
    "COINS": 1,
    "ARROWS": 5,
    "HEALTH POTION": 50,
    "MANA POTION": 50,
    "SPELLBOOK": 250,
    "SKILLBOOK": 250,
    "CLOTH": 10,
    "DUSTY TOME": 10,
    "RING": 150,
    "NECKLACE": 200
}

class Item():
    def __init__(self, item: str | Equipment, quantity = 1):
        if isinstance(item, Equipment):
            self.name = item.name
            self.is_equip = True
            self.item = item
            self.value = self.set_value()
        else:
            self.name = item
            self.is_equip = False
            self.value = self.set_value()
            #For typing reasons in other files assigning as Equipment
            self.item = Equipment("None", equipment_slot_head, 0, 0, 0, 0)

        self.quantity = quantity

    def __str__(self):
        return f"Item: {self.name} Quantity: {self.quantity}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.name == str(other)
    
    def set_value(self):
        if self.is_equip:
            value = (5 * (self.item.armor + self.item.mr)) + (2 * (self.item.phys_damage + self.item.mage_damage))
        else:
            value = prices[self.name]
        return value