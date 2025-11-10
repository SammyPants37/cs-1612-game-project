from enum import Enum
from posixpath import normpath

#Below is where we will import our constant values

def event_number_scaler(x: int) -> int: #current formula for scaling how many events will have a 1/6th chance of occurring
    return int((1 / 50) * x ** 2 + 1)

class Minerals:
    weights = [(1, 4, 5, 6, 8, 17, 18, 30, 40, 50, 110, 150, 9), # weights ordered from least to most common (real)
               (0, 12, 11, 10, 9, 17, 16, 35, 40, 50, 110, 150, 0)] # fake weights generation hehe

    # Enum classes allow the value and name of a function to be used in place of a function
    class mineralTypes(Enum):
        unminable = (0, "Worthless Rock", 0, "Congratulations! You mined a worthless rock!")
        diamond = (1, "Diamond", 100000, "Your eyes glimmer at the sight of a room laden with diamonds. You stuff your bag full of them until your hands bleed.")
        ruby = (2, "Ruby", 85000, "Your lantern lights up a crimson hue in a crevice to your side. Preparing for the worst, you investigate,\nleading your bag to become loaded with rubies.")
        emerald = (3, "Emerald", 65000, "The green shine of emeralds flash across your eyes as you cross a corner. Investigating leads to a sizable pocket,\nand a sizable profit, in your bag.")
        sapphire = (4, "Sapphire", 35000, "After passing by a small stream several times you realize the blue hue shining back at you is a gemstone!\nYou gather a good haul of sapphire, at least it’ll sell for a fortune.")
        amethyst = (5, "Amethyst", 10000, "You sing “Purple rock, purple rock, gotta love purple rocks” as you mine numerous geodes of amethysts.")
        platinum = (6, "Platinum", 5500, "You feel relieved that your bag nullifies the weight of minerals, you lug a ton of platinum into your bag.")
        gold = (7, "Gold", 3500, "You’ve heard it works pretty good as a replacement for teeth, maybe that’s why humans find it so valuable…\nyou collect a modest amount of gold hoping it’ll be worth something.")
        silver = (8, "Silver", 2500, "All the fancy dwarfs used this for cutlery, you hope it sells the same to fancy humans.\nYou store a heap of silver in your bag.")
        iron = (9, "Iron", 1750, "As a dwarf you can never complain when there’s iron involved, or at least that’s what all the village smiths said.\nYou mine a large vein of iron that’d make your ancestors proud.")
        copper = (10, "Copper", 750, "Not as good as iron, but not the worst in the world for forging. You fill your bag with wads of copper.")
        coal = (11, "Coal", 250, "Your eyes glimmer at the sight of a room laden with di–coal. Just coal. With tears in your eyes from the wasted time,\nyou begrudgingly stuff your bag with clumps of coal.")
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

devMode = False # added devMode to check if things are working as expected easier
ItemLimit = 3
NumPlayerMoves = 3
DenominatorEventsOccur = 6 # in case we would like to change the 1/6th chance they occur separately

class Items(Enum):
    nothing = 0
    dynamite = 1
    weapon = 2
    mushroom = 3

def item_weights(): # to make items more or less common
    return [40,5,5,2] # nothing, dynamite, weapon, mushroom

mapExtras = [
    "    Legend:",
    f"    ?: unexplored tile {"N":^15}",
    f"    \033[37m_\033[0m: unmineable tile {"ᐃ":^15}",
    f"    \033[31m#\033[0m: caved in tile   {"W ᐊ ✪ ᐅ E":^15}",
    f"    \033[34mP\033[0m: player          {"ᐁ":^15}",
    f"    \033[32mO\033[0m: mineral tile    {"S":^15}",
    f"    \033[36mE\033[0m: exit/escape tile",
    f"    \033[33mM\033[0m: monster infested tile",
    f"    \033[35mD\033[0m: monster den tile",
    f"    \033[100m \033[0m: tile has item"]
# refer to Tile.py, in @override to see comments for each symbol's color, main.py showMap for P

mapWidth = 25 # must be greater than 5
mapHeight = 25 # must be greater than 5

def game_objective():
    print("\033[34mYou are an aspiring dwarf\033[0m native to the Great Northern Mountains, being born\n"
    'and raised in “Zwergberg”, the dwarven village \033[34mlocated in the most Northern part\033[0m\n'
    "of the mine. Recently coming of age, you are ready to put your pickaxe to use\n"
    "and \033[32mstrike it rich!\033[0m But strange rumors have been beginning to surface that the\n"
    "mountain’s caverns and crevices, which have been safely mined safely for\n"
    "innumerable generations, are destined to \033[31mCOLLAPSE!\033[0m Strange tremors have been\n"
    "occurring more frequently, causing parts of the mine to \033[31mcave in\033[0m, and the \033[33mmine’s\n"
    "creatures\033[0m, the flesh and stone eating \033[33mMaulwurf\033[0m, have been increasingly active. You\n"
    "have decided to \033[36mhead South to escape\033[0m the mine to the sky plane before it is too\n"
    "late! Of course stuffing your pockets full of \033[32mvaluable minerals\033[0m on the way out.\n")

def game_rules():
    print(f"\033[34mEvery turn the player gets {NumPlayerMoves} major actions\033[0m, but use them wisely! After each turn there\n"
          "is a chance for a \033[31mdisastrous event\033[0m to occur: either a tile will \033[31mcave in\033[0m or the \033[33mMaulwurf\033[0m\n"
          "will migrate from their \033[35mdens\033[0m. These will only become more and more likely, and numerous,\n"
          "as the days pass by. It is imperative to \033[36mescape\033[0m before you are inevitably \033[31mtrapped\033[0m and have\n"
          "to wait to \033[31mdie\033[0m.... However, \033[34mitems\033[0m can be used to clear \033[31mcave ins\033[0m and eliminate \033[33mMaulwurf\033[0m\n"
          "from tiles, which can help you from getting \033[31mtrapped\033[0m. Make sure to \033[34mgrab them when you can!\033[0m\n"
          f"But be strategic with what you carry though; \033[34myou can only hold {ItemLimit} items in your inventory\033[0m\n"
          "at any given time. Before you \033[36mleave the mines\033[0m it is important to \033[34mamass a healthy fortune\033[0m\n"
          "and \033[34mimprove your game score\033[0m. \033[32mCoal\033[0m and \033[32mcopper\033[0m (besides those pesky \033[37mworthless rocks\033[0m) are some\n"
          "of the least valuable minerals to mine, and hence give the \033[32mlowest score\033[0m. They are also the\n"
          "\033[32mmost common minerals\033[0m to find. Collecting \033[32mrare minerals\033[0m, like \033[32mdiamonds\033[0m, give a much \033[32mhigher\n"
          "score\033[0m. \033[34mInspecting a tile is a useful way to gleam what could be on the tile\033[0m, and whether it\n"
          "is worth the \033[35mtime\033[0m and \033[35mactions\033[0m it takes to mine. However, \033[33mdon't think\033[0m seeing a \033[32mdiamond\033[0m listed\n"
          "as one of three possibilities means there is a \033[33m1/3rd chance\033[0m to get it... its probably \033[32mcoal\033[0m.\n"
          "Once (\033[31mif\033[0m) you make it to the \033[36mexit\033[0m, input \033[36mEscape to exit the mountains\033[0m with your \033[32mfortune\033[0m!")

entry_counter = 0
def maulwurf_description(entry_num):
    description_list = ("A Maulwurf is a large, monstrous creature at least twice the size of man, where the\naverage size of an adult is a little bigger than that of an adult gorilla.",
                        "Maulwurf typically travel and live alone, but may gather in large,unstoppable\nhordes once in a frenzy.",
                        "They have long snouts that extend out into a shape reminiscent of a lizard's\nskull, with nose slits like that of a horse.",
                        "A distinguishing trait is their two frontal mole-like buck teeth used to chop\noff large chunks of minerals, with venom injecting fangs to the right and left of them.",
                        "Each fang secretes a saliva like substance that liquefies rocks and bones,\nsoftens crystals, and hardens flesh.",
                        "Never does a man fear death more than when he stares down the jaws of a Maulwurf,\none can only imagine the pain of their torso being ripped clean off...",
                        "One can only imagine their spine leaking out instead of blood, with the victim's\nflesh drooping until it hardens into stone.",
                        "Inside of their mouth is an endless array of molar teeth that scatter together like a mesh.",
                        "They pulverize their meals by pushing up the bottom of their jaw, like a wave\nrising up, to grind against the dipping roof of their mouth.",
                        "The side cheeks push in opposite of the roof and floor as they drop back down,\ncrushing everything in a rhythmic spasm.",
                        "Their main body is much like that of a mole, a long chest and torso that stretches\ndown to two squatting legs.",
                        "These hind legs are slightly more elongated than a normal mole, and are bendable\nat a knee, allowing the Maulwurf to stand.",
                        "Their hind claws, as do their frontal claws, match their eyes, which reflect with\na crimson hue reminiscent of rubies and blood.",
                        "These large powerful claws are only slightly tinier than their heads when compacted\ntogether, but can spread to nearly twice the size.",
                        "These sharp, deadly scoops could stab straight through a man’s stomach,\nor an iron-laced door for that matter.",
                        "They are held up by strong, gorilla-like arms that are used as a brace when\nthey stalk slowly as a sentinel would.",
                        "When they run or dig they go on their belly and lead with their snouts, using their\nlarge arms to pull themselves forward like they are swimming through air.",
                        "Their dark brown, almost black, fur is hardened and encrusted with\ncrumbs of stone latching onto each hair.",
                        "The only way to kill a Maulwurf is to use a reliable weapon to puncture its skull\nthrough its eye socket, though even their brains wear down a weapon given enough time.",
                        "Their corpses are littered too little with rare minerals to be worth hardly anything\nthough, a bigger prize would be a Maulwurf’s egg.",
                        "Their hard exteriors are riddled with a variety of rare minerals and stones, which\nmake it a highly prized trophy that any race would respect due to the hazards it takes to collect.",
                        "No one’s yet figured out how to eat it though, or make it hatch for that matter.",
                        "Would make one wonder whether it's an egg at all if the Maulwurf didn’t guard them so ferociously....")
    print(f"--Entry #{entry_num}--\n{description_list[entry_num]}\n--Reinput to continue reading--")
    if entry_num == 22:
        return -22
    return 1

def start_game_text():
    print("Zwerg: Trial Beneath the Stone ")
    print("You descend into the mine seeking riches and glory.")
    print("Your goal; reach the escape tile and survive. But survival alone earns no glory.")
    print("To be remembered, you must mine precious minerals, defeat Maulwurf monsters, and navigate collapsing tunnels.")
    print("Each action drains your energy—move, mine, inspect and kill; so use your items wisely.")
    print("Start at the top. Escape at the end.")
    print("Between lies danger, treasure, and the chance to carve your name into the history books.")


helpText: dict[str, str] = {
    "rules": "rules: rules, r\n" +
            "    show the rules of the game",
    "objective": "objective: objective, lore, o\n" +
                "    show the objective of the game",
    "maulwurf": "maulwurf: maulwurf, read\n" +
               "    show the description of a maulwurf.\n    enter run maulwurf or continue again to show the next line of the description",
    "move": "move: move [direction]\n" +
            "    Move the player in the specified direction.\n\n"+
            "    Options:\n"+
            "        n    move the player to the north\n"+
            "        s    move the player to the south\n"+
            "        e    move the player to the east\n"+
            "        w    move the player to the west\n",
    "mine": "mine: mine, m\n" +
             "    mine the the tile that the player is on",
    "inspect": "inspect: inspect, look, l\n" +
                "    inspect the tile that the player is currently standing on",
    "map": "map: map, compass, check, c\n" +
            "    show the map of the mines",
    "grab": "grab: grab, g, pick\n"+
            "    grab the item from the tile the player is standing on.\n\n"+
            "    if there is no item on the tile, nothing will be changed.\n\n"+
            "    if there is an item on the tile and your inventory is full, you will grab the item from the tile and drop the item of the other type.",
    "use": "use: use [index] [direction], dynamite [direction], weapon [direction], mushroom [direction]\n" +
            "    use a specified item in the specified direction.\n\n"+
            "    if the item cannot be used in the direction, nothing will happen.",
    "help": "help: help [command]\n" + 
            "    If run with no command input, shows most available commands.\n\n" +
            "    If run with a command input, shows the help page for that command",
    "inventory": "inventory: inventory, i\n" + 
                "    Show the inventory of the player.",
    "quit": "quit: quit [game/quit/yes/y/q]\n" + 
            "    quits the game if given a confirmation."}

