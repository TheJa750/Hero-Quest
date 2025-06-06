import random
from Constants import *
from equipment import *

class Shop():
    def __init__(self, items: list[str], prices: dict[str, int], equipment: list[Equipment]):
        self.items = items
        self.prices = prices
        self.equipment = equipment

    def __str__(self):
        strings = ["Stock:"]
        for item in self.items:
            price = self.prices[item]
            strings.append(f"{item} - {price}G")
        return "\n".join(strings)