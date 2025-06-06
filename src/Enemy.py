import random
from characters import Character
from equipment import Equipment
from player import Player

equipment_slot_head = "head"
equipment_slot_body = "body"
equipment_slot_wep = "weapon"

class Enemy(Character):
    def __init__(self, name, stats, level = 1, growth = 1, base_exp = 20):
        #level is for scaling monsters, growth is for stat points per level (in each stat)
        super().__init__(name, stats)
        self.growth = growth

        if level > 1:
            for i in range(self.level, level + 1):
                self.level_up_enemy()

        self.exp = (base_exp * 2 * (growth - 1)) + (self.level * base_exp)

    def __str__(self):
        return f"Name: {self.name} Level: {self.level} Health: {self.health}"
    
    def level_up_enemy(self):
        self.level += 1
               
        self.add_enemy_stats(self.growth)

        #Refill health/mana and update physical damage
        self.max_health = 100 * self.constitution
        self.health = self.max_health
        self.max_mana = 25 * self.wisdom
        self.mana = self.max_mana
        self.phys_damage = ((5 * self.strength) + self.head_armor.phys_damage
                            + self.body_armor.phys_damage + self.weapon.phys_damage)
        
    def add_enemy_stats(self, per_level):
        self.strength += per_level
        self.agility += per_level
        self.constitution += per_level
        self.wisdom += per_level
        self.luck += per_level

    def create_random_loot(self, player: Player):
        loot = {"item": 1}
        return loot

    def death(self, player: Player):
        print(f"{player.name} gains {self.exp} from slaying {self.name}.")
        player.gain_exp(self.exp)
        loot = self.create_random_loot(player) #dictionary [str, int] OR [str, Equipment]

        #loop to add to player invent and print loot message
        for item_key in loot:
            item = loot[item_key]
            if isinstance(item, Equipment):
                player.invent[item.name] = item
                print(f"{item_key} has been added to {player.name}'s inventory.")
            else:
                player.invent[item_key] = item
                print(f"{item_key} x {item} has been added to {player.name}'s inventory.")