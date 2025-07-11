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
            "CLOTH", "COINS", "RING", "NECKLACE", "FRUIT"
        ]
        weights = [12, 12, 6, 6, 35, 35, 80, 3, 3, 1]

        print(f"DEBUG: mod: {luck_mod} growth: {self.growth}")
        num_rolls = random.randint(1, luck_mod + self.growth)
        print(f"DEBUG: rolls: {num_rolls}")

        while num_rolls > 0:
            equip_rolls = 0
            equip_roll = random.randint(0, 300 * (equip_rolls + 1))
            if 5 + player.luck >= equip_roll & num_rolls > 1:
                print("DEBUG: Rolled equipment")
                item = Item(create_new_equipment(player))
                loot.append(item)
                num_rolls -= 3
                equip_rolls += 1
            else:
                print("DEBUG: Failed equipment roll")
                item_rolls = random.randint(1, num_rolls)
                print(f"DEBUG: Rolling {item_rolls} items")
                items = random.choices(item_list, weights, k=item_rolls)
                num_rolls -= item_rolls
                for item in items:
                    match item:
                        case "COINS":
                            modifier = self.level + (2 * self.growth)
                            quantity = random.randint(10, 5 * modifier)
                        case "CLOTH", "DUSTY TOME":
                            modifier = self.level + (2 * self.growth)
                            quantity = random.randint(2, 2 + modifier)
                        case _:
                            quantity = 1
                    name = item
                    if item == "FRUIT":
                        stats = ["STRENGTH", "AGILITY", "CONSTITUTION", "WISDOM", "LUCK", "ASCENSION", "BLOODTHIRST"]
                        stat_weights = [100, 100, 100, 100, 15, 1, 5]
                        stat = random.choices(stats, stat_weights)
                        name = item + " OF " + stat[0]
                    exists = False
                    for obj in loot:
                        if obj.name == name:
                            obj.quantity += quantity
                            exists = True
                    if not exists:
                        loot.append(Item(name, quantity))

        return loot #type: list[Item]

    def death(self, player: Player):
        print(f"{player.name} gains {self.exp} exp from slaying {self.name}.")
        player.gain_exp(self.exp)
        loot = self.create_random_loot(player) #list of Item objects

        #loop to add to player invent and print loot message
        for obj in loot:
            print(f"{player.name} recieves {obj} from {self.name}")
            player.add_to_invent(obj)
