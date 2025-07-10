import random
from Constants import *
from equipment import *
from player import Player
from item import Item

basic_items = [
    "HEALTH POTION",
    "MANA POTION",
    "SPELLBOOK",
    "SKILLBOOK"
]

weights = [75, 75, 1, 1]


class Shop():
    def __init__(self, markup: float, player: Player):
        self.items = []
        self.prices = []
        self.player = player
        self.base_markup = markup
        self.markup = markup - (0.01 * player.luck)
        self.restock_items()

    def restock_items(self):
        #Clear old inventory first
        self.items.clear()
        self.prices.clear()

        #Determine number of base stock item rolls using player luck
        item_rolls = self.player.luck // 2

        #Add each item to shop stock
        choice_list = basic_items.copy()
        weights_list = weights.copy()
        if self.player.style == "Archer":
            choice_list.append("ARROWS")
            weights_list.append(100)
        items_choices = random.choices(choice_list, weights=weights_list, k=item_rolls)
        
        items = []
        for item in items_choices:
            match item:
                case "HEALTH POTION":
                    items.append(Item("HEALTH POTION", 1))
                case "MANA POTION":
                    items.append(Item("MANA POTION", 1))
                case "SPELLBOOK":
                    items.append(Item("SPELLBOOK", 1))
                case "SKILLBOOK":
                    items.append(Item("SKILLBOOK", 1))
                case "ARROWS":
                    items.append(Item("ARROWS", 5))
        items.append(Item("HEALTH POTION", 2))  # Always add health potions
        items.append(Item("MANA POTION", 2))  # Always add mana potions

        for item in items:
            self.add_to_items(item)

        #Determine number of equipment rolls using player luck
        num_equip = random.randint(int(round(self.player.luck/7)), int(round(self.player.luck)/3))

        #Add each new equipment to the shop stock
        for i in range(num_equip):
            item = create_new_equipment(self.player)
            self.items.append(Item(item))

        #Update markup based on player luck
        self.markup = self.base_markup - (0.01 * self.player.luck)

        #Update prices for new stock
        for item in self.items:
            self.prices.append(round(item.value * self.markup))

    def __str__(self):
        strings = ["Stock:"]
        for i in range(len(self.items)):
            item = self.items[i]
            price = self.prices[i]
            strings.append(f"{item} - {price}G")
        return "\n".join(strings)
    
    def add_to_items(self, item: Item):
        exists, index = self.check_for_item(item.name)
        if exists:
            self.items[index].quantity += item.quantity
        else:
            self.items.append(item)

    def check_for_item(self, item_name: str):
        exists = False
        index = -1
        for obj in self.items:
            if obj == item_name:
                index = self.items.index(obj)
                exists = True
        return exists, index 
    
    def buy_item(self, index: int):
        money = self.player.get_item("COINS") 

        item = self.items[index]
        price = self.prices[index]

        print(f"Debug: {item.name} has value {item.value} and price {price} with markup {self.markup}")

        if item.is_equip:
            slot = item.item.slot
            amount = 1
            if slot == "head":
                self.player.head_armor.compare_equipment(item.item)
            elif slot == "body":
                self.player.body_armor.compare_equipment(item.item)
            else:
                self.player.weapon.compare_equipment(item.item)
        else:
            prompt = f"How many {item.name} would you like to buy? (0 - {item.quantity})"
            valid_inputs = ["0"]
            for i in range(item.quantity):
                valid_inputs.append(f"{i+1}")
            amount = int(validate_input(prompt, valid_inputs, "Please enter a valid amount."))
        
        cost = price * amount
        
        print(f"{item.name} will cost {cost} coins. You have {money.quantity} coins.") #type: ignore

        if not user_yes_no_check(item.name, "buy"):
            return
        
        if money.quantity < cost: #type: ignore
            print("Insufficient funds, please come back richer.")
            return
        else:
            money.quantity -= cost #type: ignore

            if item.is_equip:
                purchase = Item(item.item, amount)
            else:
                purchase = Item(item.name, amount)
            self.player.add_to_invent(purchase)
            item.quantity -= amount

            if item.quantity == 0:
                self.items.remove(item)

            print(f"{self.player.name} pays {cost} coins to the cashier.")
            print(f"{item.name} has been added to inventory.")

    def sell_item(self):
        #Determine which item player wants to sell
        strings = ["Inventory:", "0 = Back"]
        valid = ["0"]

        for i in range(len(self.player.invent)):
            item = self.player.invent[i]
            strings.append(f"{i+1} = {item}")
            valid.append(f"{i+1}")
        
        prompt = "\n".join(strings)
        choice = int(validate_input(prompt, valid))

        if choice == 0: #back was selected, return to shop menu
            return

        #Get the Item object from player inventory
        item = self.player.invent[choice-1] #type: Item

        #Check if item is equipment or not for setting sell amount
        if item.is_equip:
            amount = 1
        elif item.name == "COINS":
            print("Nice try wise guy.")
            return
        else:
            prompt = f"How many {item.name} would you like to sell? (0 - {item.quantity})"
            valid_inputs = ["0"]
            for i in range(item.quantity):
                valid_inputs.append(f"{i+1}")
            amount = int(validate_input(prompt, valid_inputs, "Please enter a valid amount."))

        coins = round(item.value * amount * 0.7) #Shop buys for 70% of value
        final_warning = f"Are you sure you would like to sell {item.name} x {amount} for {coins} coins?\nWarning: items will be lost forever once sold.\n1 = Yes\n2 = No"
        sell = validate_input(final_warning, ["1", "2"])

        if sell == "2": #No was selected, return to shop menu
            return

        
        self.player.add_to_invent(Item("COINS", coins))
        item.quantity -= amount
        print(f"{self.player.name} hands over {amount} {item.name} and recieves {coins} coins.")

        if item.quantity == 0: #if all are sold, remove from inventory.
            self.player.invent.remove(item)

def user_yes_no_check(item, function: str):
    prompt = f"Would you like to {function} {item}?\n1 = Yes\n2 = No"
    choice = validate_input(prompt, ["1", "2"])

    if choice == "1":
        return True
    else:
        return False