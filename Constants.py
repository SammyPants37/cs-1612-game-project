from enum import Enum

#Below is where we will import our constant values

def event_number_scaler(x: int) -> int: #current formula for scaling how many events will have a 1/6th chance of occurring
    return int((1 / 50) * x ** 2 + 1)

class Minerals:
    weights = [1, 4, 5, 6, 8, 17, 18, 30, 40, 50, 110, 200, 9]  # weights ordered from least to most common

    # Enum classes allow the value and name of a function to be used in place of a function
    class mineralTypes(Enum):
        unminable = (0, "Worthless Rock", 0, "Congratulations! You mined a worthless rock!")
        diamond = (1, "Diamond", 100000, "Your eyes glimmer at the sight of a room laden with diamonds. You stuff your bag full of them until your hands bleed.")
        ruby = (2, "Ruby", 85000, "Your lantern lights up a crimson hue in a crevice to your side.  Preparing for the worst, you investigate, leading your bag to become loaded with rubies.")
        emerald = (3, "Emerald", 65000, "The green shine of emeralds flash across your eyes as you cross a corner. Investigating leads to a sizable pocket, and a sizable profit in your bag.")
        sapphire = (4, "Sapphire", 35000, "After passing by a small stream several times you realize the blue hue shining back at you is a gemstone! You gather a good haul of sapphire, at least it’ll sell for a fortune.")
        amethyst = (5, "Amethyst", 10000, "You sing “Purple rock, purple rock, gotta love purple rocks” as you mine numerous geodes of amethysts.")
        platinum = (6, "Platinum", 5500, "You feel relieved that your bag nullifies the weight of minerals, you lug a ton of platinum into your bag.")
        gold = (7, "Gold", 3500, "You’ve heard it works pretty good as a replacement for teeth, maybe that’s why humans find it so valuable… you collect a modest amount of gold hoping it’ll be worth something.")
        silver = (8, "Silver", 2500, "All the fancy dwarfs used this for cutlery, you hope it sells the same to fancy humans. You store a heap of silver in your bag.")
        iron = (9, "Iron", 1750, "As a dwarf you can never complain when there’s iron involved, or at least that’s what all the village smiths said. You mine a large vein of iron that’d make your ancestors proud.")
        copper = (10, "Copper", 750, "Not as good as iron, but not the worst in the world for forging. You fill your bag with wads of copper.")
        coal = (11, "Coal", 250, "Your eyes glimmer at the sight of a room laden with di–coal. Just coal. With tears in your eyes from the wasted time, you begrudgingly stuff your bag with clumps of coal.")
        monsterDen = (12, "Maulwurf Egg", 6000, "you hack away at the maulwurf den and are surprised to find that you receive a maulwurf egg for your troubles.")

        # expanding on an Enum with a __init__ allows more than value and name to be associated with a variable
        def __init__(self, code: int, description: str, score_value: int, miningDescription: str):
            self.code = code
            self.description = description
            self.score_value = score_value
            self.miningDescription = miningDescription
            """ print(Minerals.mineralTypes.diamond.name) # diamond
            print(Minerals.mineralTypes.diamond.value) # (0, "Diamond", 100000)
            print(Minerals.mineralTypes.diamond.code) # 0
            print(Minerals.mineralTypes.diamond.description) # Diamond
            print(Minerals.mineralTypes.diamond.score_value) # 100000 """

ItemLimit = 3
NumPlayerMoves = 3
DenominatorEventsOccur = 6 # in case we would like to change the 1/6th chance they occur separately

class Items(Enum):
    nothing = 0
    dynamite = 1
    weapon = 2

def item_weights(): # to make items more or less common
    return [40,5,5] # nothing, dynamite, weapon

mapExtras = [
    "	Legend:",
    "	?: unexplored tile		    N",
    "	\033[37m_\033[0m: unmineable tile		    ᐃ",
    "	\033[31m#\033[0m: caved in tile		W ᐊ ⚪ ᐅ E",
    "	\033[36mP\033[0m: player			    ᐁ",
    "	\033[32mO\033[0m: mineral tile			    S",
    "	\033[34mE\033[0m: exit/escape tile		",
    "	\033[33mM\033[0m: monster infested tile",
    "	\033[35mD\033[0m: monster den tile		"]
# refer to Tile.py, in @override to see comments for each symbol's color, main.py showMap for P

mapWidth = 25
mapHeight = 25

