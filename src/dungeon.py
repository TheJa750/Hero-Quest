import random
from Enemy import Enemy
from characters import get_starting_stats
from Constants import *

class Dungeon():
    def __init__(self, name: str, num_floors: int, difficulty: int, info: list, player_lvl: int, rooms_per_floor = 2):
        self.name = name
        self.floors = []
        self.diff = difficulty
        self.rooms = rooms_per_floor
        self.info = info
        self.player = player_lvl

        for i in range(num_floors):
            floor = self.create_floor(i+1)
            self.floors.append(floor)

    def create_floor(self, floor_num):
        name = f"{self.name} Floor {floor_num}"
        return Floor(name, self)
    
    def __str__(self):
        return f"Dungeon: {self.name} Floors: {len(self.floors)} Rooms/Floor: {self.rooms}"
    
    def __repr__(self):
        strings = [f"{self.name}"]
        for floor in self.floors:
            strings.append(repr(floor))
            for room in floor.rooms:
                strings.append(repr(room))
        return "\n".join(strings)
    
    def __len__(self):
        count = 0
        for floor in self.floors:
            for room in floor.rooms:
                count += 1
        return count

    def next_room(self):
        while len(self.floors) > 0: #If dungeon has floors remaining
            floor = self.floors[0] #type: Floor
            if len(floor.rooms) > 0: #If floor has rooms remaining
                return floor.rooms.pop(0) #return (and remove) next room in list
            else:                      #If floor has no rooms remaining
                self.floors.remove(floor) #remove the floor from the list
        return f"Congratulations! {self.name} has been conquered!"

class Floor():
    def __init__(self, name: str, dungeon: Dungeon):
        self.name = name
        self.rooms = []
        self.diff = dungeon.diff
        self.info = dungeon.info
        self.player = dungeon.player

        for i in range(dungeon.rooms):
            
            room = self.create_room(i+1, i == dungeon.rooms - 1)
            self.rooms.append(room)
    
    def create_room(self, room_num, boss = False):
        name = f"{self.name}-{room_num}"
        if self.diff > 1:
            enemies = round(self.diff / 2)
        else:
            enemies = 1
        
        return Room(name, self, boss, enemies)
    
    def __str__(self):
        return f"{self.name} Rooms: {len(self.rooms)}"
    
    def __repr__(self):
        strings = [f"{self.name}"]
        for room in self.rooms:
            strings.append(repr(room))
        return "\n".join(strings)

    def __len__(self):
        return len(self.rooms)

class Room():
    def __init__(self, name: str, floor: Floor, boss_room = False, num_enemies = 1):
        self.name = name
        self.diff = floor.diff
        self.enemies = []

        basic_names = floor.info[0].copy()
        boss_names = floor.info[1].copy()

        random.shuffle(basic_names)
        random.shuffle(boss_names)

        if floor.player <=5:
            scaling = 1
        elif 5 < floor.player <= 10:
            scaling = 2
        elif 10 < floor.player <= 20:
            scaling = 3
        else:
            scaling = 5

        for i in range(num_enemies):
            enemy_name = random.choice(basic_names)
            enemy = self.create_enemy(enemy_name, self.diff, scaling, False, floor.player)
            self.enemies.append(enemy)

        if boss_room:
            enemy_name = random.choice(boss_names)
            Boss = self.create_enemy(enemy_name, self.diff, scaling, True, floor.player)
            self.enemies.append(Boss)

    def __str__(self):
        return f"{self.name} - Enemies: {len(self.enemies)}"
    
    def __len__(self):
        return len(self.enemies)
    
    def __repr__(self):
        strings = [f"{self.name}"]
        for enemy in self.enemies:
            strings.append(str(enemy))
        return "\n".join(strings)
    
    def create_enemy(self, name: str, difficulty: int, scaling: int, boss: bool, player_lvl: int):
        level = random.randint(player_lvl - 2, player_lvl + 2)
        if boss:
            stats = get_starting_stats(difficulty * scaling * 20)
            growth = 3
            level = player_lvl + 2
            base_exp = 50
        else:
            stats = get_starting_stats(difficulty * scaling * 10)
            growth = 1
            base_exp = 20

        return Enemy(name, stats, level, growth, base_exp)



