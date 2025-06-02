import random
from characters import Character
from equipment import Equipment

equipment_slot_head = "head"
equipment_slot_body = "body"
equipment_slot_wep = "weapon"

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
    
    def basic_shot(self, target: Character):
        if self.invent['ARROWS'] > 0:
            print(f"{self.name} shoots {target.name}.")
            self.invent['ARROWS'] -= 1
            target.take_damage(self.phys_damage, "physical")

    def double_shot(self, target: Character):
        # Fires 2 arrows back to back, the second one has a 70% chance to hit for 75% of base damage
        print(f"{self.name} uses Double Shot to attack {target.name}.")
        hit_chance = random.randint(0, 100)
        if hit_chance >= 30:
            pass

    def piercing_shot(self, target: Character):
        pass