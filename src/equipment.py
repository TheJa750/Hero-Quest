import random
from Constants import *

class Equipment():
    def __init__(self, name, slot, armor, mr, melee_damage, mage_dmg):
        self.name = name
        self.slot = slot
        self.armor = armor
        self.mr = mr
        self.phys_damage = melee_damage
        self.mage_damage = mage_dmg
    
    def __str__(self) -> str:
        return f"{self.name}:\n\
            Slot: {self.slot}\n\
            Armor: {self.armor}\n\
            Magic Resist: {self.mr}\n\
            Physical Damage: {self.phys_damage}\n\
            Magical Damage: {self.mage_damage}"
    
    def compare_equipment(self, other):
        print("Equipped vs. New")
        print(f"Name: {self.name} vs. {other.name}")
        print(f"Armor: {self.armor} vs. {other.armor}")
        print(f"Magic Resist: {self.mr} vs. {other.mr}")
        print(f"Phyiscal Damage: {self.phys_damage} vs. {other.phys_damage}")
        print(f"Magical Damage: {self.mage_damage} vs. {other.mage_damage}")

    def __repr__(self) -> str:
        return f"S:{self.slot}, A:{self.armor}, R:{self.mr}, P:{self.phys_damage}, M:{self.mage_damage}"
    
def create_new_equipment(player):
    luck_mod = int(round(player.luck / 3))
    if player.level <= 5:
        def_points = random.randint(0, 3 + luck_mod)
        dmg_points = random.randint(5, 15 + luck_mod)
    elif 5 < player.level <= 10:
        def_points = random.randint(5, 7 + luck_mod)
        dmg_points = random.randint(12, 25 + luck_mod)
    elif 10 < player.level <= 20:
        def_points = random.randint(10, 20 + luck_mod)
        dmg_points = random.randint(30, 50 + luck_mod)
    else:
        def_points = random.randint(25, 40 + luck_mod)
        dmg_points = random.randint(60, 90 + luck_mod)

    armor, mr = 0, 0
    phys, mage = 0, 0

    while def_points > 0:
        choice = random.choice(["armor", "mr"])
        if choice == "armor":
            armor += 1
        else:
            mr += 1
        def_points -= 1

    while dmg_points > 0:
        choice = random.choice(["phys", "mage"])
        if choice == "phys":
            phys += 1
        else:
            mage += 1
        dmg_points -= 1

    slot = random.choice(["weapon", "head", "body"])

    if player.style == "Mage":
        wep = "Staff"
        head = "Hat"
        body = "Robes"
    elif player.style == "Archer":
        wep = "Bow"
        head = "Coif"
        body = "Scale Armor"
    else:
        wep = "Sword"
        head = "Helm"
        body = "Plate Armor"

    prename = random.choice(prename_modifiers)
    postname = random.choice(postname_modifiers)

    if slot == "weapon":
        name = f"{prename} {wep} of {postname}"
    elif slot == "head":
        name = f"{prename} {head} of {postname}"
    else:
        name = f"{prename} {body} of {postname}"

    return Equipment(name, slot, armor, mr, phys, mage)
