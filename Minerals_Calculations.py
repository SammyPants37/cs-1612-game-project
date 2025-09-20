import random
from enum import Enum

class MineralNumbers:
    def __init__(self):
        self.mineral_tile_amount = 24  # amount of mineral tiles on the board
        self.mineral_weights = [1, 4, 5, 6, 8, 17, 18, 30, 40, 50, 110, 200]  # weights ordered from least to most common
        self.mineral_codes = list(range(12))  # creates a list of values from 0 to 11, corresponding to each mineral
MN = MineralNumbers()

# Enum classes allow the value and name of a function to be used in place of a function
class EnumMineral(Enum):
    unminable = (0, "{Unminable}", None)
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

def mineral_tile_func():
    """ # Creates a list of the minerals which can be later assigned to individual tiles.
Random.choices is an expanded form of random.choice, which outputs a list instead of a single number, the
biggest benefits are it allows weighted probability and is easily scalable. To explain what each part does, 
first is the "population" variable, or (mineral_codes, . . .), what it does is names how many things we have
to choose from [which corresponds to each mineral code]. The number of things in the population must match up
with how many items are in a weight, or (..., weights = mineral_weights, ... , and then they will be assigned 
via order, i.e., 0 is assigned a weight of 1, 1 is assigned a weight of 4, . . . and 11 is assigned a weight 
of 200 [more numbers in a weight corresponds to a greater probability they will be chosen]. Lastly, k is the
random.choices function's chosen dummy variable which corresponds to how many numbers will be put into the
final list. So, if k = 1 then only mineral will be randomly chosen and put in the list. For our game k will
be set at whatever the amount of mineral tiles we eventually decide on and therefore will assign a value to. 
Printing (mineral_list_weighted) will show a list of all our codes that were randomly generated"""
    mineral_list_weighted = random.choices(MN.mineral_codes, weights = MN.mineral_weights, k = MN.mineral_tile_amount)

    """ Defines the dictionary function that will associate my Enum values to their random number in the weight (if any).
It can be broken up into two main parts {m.code: m ...}, the main dictionary, and {... for m in Mineral}, the loop.
It is worth noting that [m] is just a dummy variable interchangeable with any other. 
The loop is easier to explain first. What it does is add m to our list when we find it in our class Mineral. 
But without the dictionary all we would be doing is seeing if its name, e.g., "diamond", shows up in our variable m. 
The dictionary allows us to see if the code value is in the class Mineral, instead of just its name. E.g., with
the name "diamond" in m {m.code : m ...} would be equivalent to {diamond.code : diamond ...} [or {1 : diamond}], 
making it so they can be used interchangeably in the loop (but not outside). This is great for us since our 
probabilities are assigned to the mineral's code not name. """
    code_to_mineral = {m.code: m for m in EnumMineral}

    """ Below is partially from P4E pg. 114 (pg. 127 pdf) 9.3 Looping and dictionaries. To explain,
    every_code is an interchangeable dummy variable. What "for every_code in mineral_list_weighted:"
    does is "traverses the keys in the dictionary", or in terms that make more sense, it does something
    for each thing in finds in the dictionary. Inside this loop we create a front variable that we can
    attach to our Enum classes, so .code, .name., .description, .score_value would all technically work
    in tangent with the variable mineral. We set it equal to "code_to_mineral[every_code]" since this will
    associate the dictionary code_to_mineral and its assigned output []. We make the outputs every_code 
    since this will compare the entire list of values (while something like [1] would just make the mineral 
    variable diamonds for every item in the list). When it is our dummy variable it will compare all its keys
    to find which ones are in the list, and then once found it can also do its output function. """
    for every_code in mineral_list_weighted: # "traverses" the keys in mineral_list_weighted
        mineral = code_to_mineral[every_code] #creates a front variable that we can attach to our Enum codes
        #mineral.code = TilesClass.mineral_tile[TilesClass.tile_number_variable]
        # TilesClass.tile_number_variable += 1

# mineral_tile_func()