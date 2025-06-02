import random
from characters import Character
from equipment import Equipment

equipment_slot_head = "head"
equipment_slot_body = "body"
equipment_slot_wep = "weapon"

class Mage(Character):
    def __init__(self, name, stats, spells):
        super().__init__(name, stats)
        for spell in spells:
            self.spells.append(spell)

        starting_gear = [Equipment("Starter's Wand", equipment_slot_wep, 0, 2, 5, 10),
                         Equipment("Dusty Hat", equipment_slot_head, 1, 2, 0, 1)]
        
        for gear in starting_gear:
            self.equip_item(gear)
        
    def cast_fireball(self, target):
        print(f"{self.name} attempts to cast Fireball at {target.name}.")
        base_dmg = 50
        mana_cost = 25
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = base_dmg + (self.wisdom * 5) + self.mage_damage
            target.take_damage(damage, "magical")
            print(f"Fireball hits {target.name} for {max(0, damage - (target.magic_resist * 5))} magical damage.")
        else:
            print(f"{self.name} has insufficient mana to cast Fireball.")
    
    def cast_chain_lightning(self, target):
        print(f"{self.name} attempts to cast Chain Lightning at {target.name}.")
        base_dmg = 30
        mana_cost = 10
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = base_dmg + (self.wisdom * 2.5) + self.mage_damage
            target.take_damage(damage, "magical")
            print(f"Chain Lightning hits {target.name} for {max(0, damage - (target.magic_resist * 5))} magical damage.")
        else:
            print(f"{self.name} has insufficient mana to cast Chain Lightning.")
        
    def cast_shadow_fangs(self, target):
        # Shadow Fangs - strikes target twice, each one gets offensive bonuses to damage, but also defensive reduction to damage.
        print(f"{self.name} attempts to cast Shadow Fangs at {target.name}.")
        base_dmg = 20
        mana_cost = 20
        if self.mana - mana_cost >= 0:
            self.mana -= mana_cost
            damage = base_dmg + (self.wisdom * 2.5) + self.mage_damage
            target.take_damage(damage, "magical")
            print(f"Shadow Fangs hits {target.name} for {max(0, damage - (target.magic_resist * 5))} magical damage.")
            target.take_damage(damage, "magical")
            print(f"Shadow Fangs hits {target.name} for {max(0, damage - (target.magic_resist * 5))} magical damage.")
        else:
            print(f"{self.name} has insufficient mana to cast Shadow Fangs.")