from enum import Enum

#Below is where we will import our constant values

def event_number_scaler(x): #current formula for scaling how many events will have a 1/6th chance of occurring
    return int((1 / 50) * x ** 2 + 1)

class Minerals:
    tile_amount = 24  # amount of mineral tiles on the board
    weights = [1, 4, 5, 6, 8, 17, 18, 30, 40, 50, 110, 200]  # weights ordered from least to most common
    codes = list(range(12))  # creates a list of values from 0 to 11, corresponding to each mineral

    # Enum classes allow the value and name of a function to be used in place of a function
    class Enum(Enum):
        unminable = (0, "{Worthless Rock}", 0)
        diamond = (1, "Diamond", 100000)
        ruby = (2, "Ruby", 85000)
        emerald = (3, "Emerald", 65000)
        sapphire = (4, "Sapphire", 35000)
        amethyst = (5, "Amethyst", 10000)
        platinum = (6, "Platinum", 5500)
        gold = (7, "Gold", 3500)
        silver = (8, "Silver", 2500)
        iron = (9, "Iron", 1750)
        copper = (10, "Copper", 750)
        coal = (11, "Coal", 250)

        # expanding on an Enum with a __init__ allows more than value and name to be associated with a variable
        def __init__(self, code, description, score_value):
            self.code = code
            self.description = description
            self.score_value = score_value
            """ print(Mineral.diamond.name) # diamond
        print(Mineral.diamond.value) # (0, 'Diamond', 100000)
        print(Mineral.diamond.code) # 0
        print(Mineral.diamond.description) # Diamond
        print(Mineral.diamond.score_value) # 100000 """

ItemLimit = 3
NumPlayerMoves = 3
DenominatorEventsOccur = 6 # in case we would like to change the 1/6th chance they occur separately

