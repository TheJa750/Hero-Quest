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
    
    def basic_shot(self, target: Character,dmg_mod = 1.0, dmg_type = "physical"):
        if self.invent['ARROWS'] > 0:
            print(f"{self.name} shoots {target.name}.")
            self.invent['ARROWS'] -= 1
            target.take_damage(dmg_mod * self.phys_damage, dmg_type)
            print(f"Arrows remaining: {self.invent['ARROWS']}.")
        else:
            print("Not enough arrows!")
            self.melee_strike(target)
        return True

    def double_shot(self, target: Character):
        # Fires 2 arrows back to back, the second one has a 70% chance to hit for 75% of base damage
        print(f"{self.name} uses Double Shot to attack {target.name}.")
        self.basic_shot(target)
        hit_chance = random.randint(0, 100)
        if hit_chance >= 30:
            self.basic_shot(target, 0.75)
        else:
            print(f"{self.name}'s 2nd shot misses.")
        return True

    def piercing_shot(self, target: Character):
        #Fires a shot that ignores armor
        print(f"{self.name} uses Piercing Shot to attack {target.name}.")
        self.basic_shot(target, dmg_type="true")
        return True