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
    
    def cleave(self, target1, target2 = None, target3 = None):
        #Targets up to 3 enemies target1 is main target and gets full damage, target2/3 get 75% damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} cleaves {target1.name}.")
        target1.take_damage(dmg, "physical")

        if target2 and target3:
            print(f"The sweep hits {target2.name} and {target3.name}.")
            target2.take_damage(0.75 * dmg, "physical")
            target3.take_damage(0.75 * dmg, "physical")
        elif target2:
            print(f"The sweep hits {target2.name}.")
            target2.take_damage(0.75 * dmg, "physical")
        elif target3:
            print(f"The sweep hits {target3.name}.")
            target3.take_damage(0.75 * dmg, "physical")
        else:
            print("No other targets in range.")

        return True

    def devastating_strike(self, target):
        #Deals true damage
        dmg = max(1, self.phys_damage)
        print(f"{self.name} lands a powerful blow on {target.name}.")
        target.take_damage(dmg, "true")

        return True

    def fury_of_blows(self, target):
        #Attacks a random number of times (2-5 inclusive), each for 50% damage
        num_attacks = random.randint(2,5)
        dmg = max(1, 0.5 * self.phys_damage)
        print(f"{self.name} quickly attacks {target.name} {num_attacks} times.")
        for i in range(0, num_attacks):
            target.take_damage(dmg, "physical")
        return True
