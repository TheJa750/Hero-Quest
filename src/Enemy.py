import random
from characters import Character
from equipment import Equipment, create_new_equipment
from player import Player
from shop import Item

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

        self.exp = (base_exp * 2 * (growth - 1)) + (self.level * base_exp) + 10

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
        luck_mod = 1 + round(player.luck / 10)
        loot = []

        item_list = [
            "HEALTH POTION", "MANA POTION",
            "SPELLBOOK", "SKILLBOOK", "DUSTY TOME",
            "CLOTH", "COINS", "RING", "NECKLACE" 
        ]
        weights = [5, 5, 2, 2, 25, 25, 50, 1, 1]

        num_rolls = random.randint(1, luck_mod)

        equip_roll = random.randint(0, 300)

        if 5 + player.luck >= equip_roll:
            item = Item(create_new_equipment(player))
            loot.append(item)
        else:
            items = random.choices(item_list, weights, k=num_rolls)
            for item in items:
                match item:
                    case "COINS":
                        modifier = self.level + (2 * self.growth)
                        quantity = random.randint(25, 25 * modifier)
                    case "CLOTH", "DUSTY TOME":
                        modifier = self.level + (2 * self.growth)
                        quantity = random.randint(2, 2 + modifier)
                    case _:
                        quantity = 1
                exists = False
                for obj in loot:
                    if obj.name == item:
                        obj.quantity += quantity
                        exists = True
                if not exists:
                    loot.append(Item(item, quantity))

        return loot #type: list[Item]

    def death(self, player: Player):
        print(f"{player.name} gains {self.exp} exp from slaying {self.name}.")
        player.gain_exp(self.exp)
        loot = self.create_random_loot(player) #list of Item objects

        #loop to add to player invent and print loot message
        for obj in loot:
            print(f"{player.name} recieves {obj} from {self.name}")
            player.add_to_invent(obj)
