import random
from characters import Character
from equipment import Equipment

equipment_slot_head = "head"
equipment_slot_body = "body"
equipment_slot_wep = "weapon"

class Warrior(Character):
    def __init__(self, name, stats, skills):
        super().__init__(name, stats)
        for skill in skills:
            self.skills.append(skill)

        starting_gear = [Equipment("Starter's Sword", equipment_slot_wep, 1, -1, 10, 0),
                         Equipment("Loose Chainmail", equipment_slot_body, 3, 0, 0, 0)]
        
        for gear in starting_gear:
            self.equip_item(gear)
    
    def cleave(self, target):
        pass

    def devastating_strike(self, target):
        pass

    def fury_of_blows(self, target):
        pass