from enum import Enum

#Below is where we will import our constant values

def zwerg_calendar_system(days_passed): # created a calendar system not based on celestial phenomena
    year = 625177
    month = 1
    weekdays = {1 : "Agaricus", 2 : "Procambarus", 3 : "Proteus", 4 : "Conecsimus"}
    months = {1 : "Dreiundfzer", 2 : "Einundfzer", 3 : "Dreiunver", 4 : "Neunzehnver", 5 : "Neunieber", 6 : "Dreicember",}
    month_name = months[month]
    while days_passed > 59:
        days_passed -= 59
        year += 1
    day_of_month = days_passed
    if days_passed > 17:
        week = ((days_passed - 18) // 3) + 6
        weekday_num = (days_passed - 17) - (week - 6) * 3
        day_of_week = weekdays[weekday_num]
    elif days_passed > 13:
        week = 5
        weekday_num = days_passed - 13
        day_of_week = weekdays[weekday_num]
    elif days_passed > 4:
        week = ((days_passed - 5) // 3) + 2
        weekday_num = (days_passed - 4) - ((week - 2) * 3)
        day_of_week = weekdays[weekday_num]
    else: # days_passed > 0:
        week = 1
        weekday_num = days_passed
        day_of_week = weekdays[weekday_num]
    if week > 4:
        month = ((week - 5) // 3) + 2
        month_name = months[month]
        day_of_month = days_passed - 13
    if month > 2:
        day_of_month = (days_passed - 23) - (9 * (month - 3))
    info = [day_of_week, week, month, day_of_month, month_name, year, weekday_num]
    return info

def event_number_scaler(x: int) -> int: # formula for scaling how many events will have a 1/6th chance of occurring
    return int((1 / 50) * x ** 2 + 1)

event_weights = (5,4) # weights for choosing which event occurs. (infest, cave in)

class AnsiColors:
    def red(self, text):
        return f"\033[31m{text}\033[0m"
    def green(self, text):
        return f"\033[32m{text}\033[0m"
    def yellow(self, text):
        return f"\033[33m{text}\033[0m"
    def blue(self, text):
        return f"\033[34m{text}\033[0m"
    def purple(self, text):
        return f"\033[35m{text}\033[0m"
    def cyan(self, text):
        return f"\033[36m{text}\033[0m"
    def gray(self, text):
        return f"\033[37m{text}\033[0m"
    def graybgrd(self, text):
        return f"\033[100m{text}"
    def italics(self, text):
        return f"\033[3m{text}\033[0m"
    def g_bold(self, text):
        return f"\033[1:32m{text}\033[0m"
    def b_bold(self, text):
        return f"\033[1:34m{text}\033[0m"
    def b_italics(self, text):
        return f"\033[3:34m{text}\033[0m"
    def bold_to_ital(self, text):
        return f"\033[1m{text}\033[22m"
    def reset(self):
        return "\033[0m"
    def purp_ydash(self, text): # creates a bold yellow dash through the preceding character (purple)
        return f"\033[35m{text}\033[1:33m\u0336\033[0m"

ansi: AnsiColors = AnsiColors()


class Minerals:
    weights = [(1, 4, 5, 6, 8, 17, 18, 30, 40, 50, 110, 175, 9, 0), # real weights, ordered the same as mineralTypes(Enum)
               (0, 2, 3, 5, 7, 12, 15, 35, 40, 48, 110, 225, 0, 0)] # fake weights for map generation

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
        monsterDen = (12, "Maulwurf Egg", 17500, "You hack away at the Maulwurf den and are surprised to find that you receive a Maulwurf egg for your troubles.")
        maulwurf = (13, "Maulwurf Remains", 8250, "After gouging through the eyes of a cavern full of Maulwurf you lay your battered weapon to rest")

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
ItemLimit = 4
NumPlayerMoves = 3
DenominatorEventsOccur = 6 # in case we would like to change the 1/6th chance they occur separately

class Items(Enum):
    nothing = 0
    dynamite = 1
    weapon = 2
    mushroom = 3

def item_weights(): # to make items more or less common
    return [38,5,5,2] # nothing, dynamite, weapon, mushroom

mapExtras = [
    "    Legend:",
    f"    ?: unexplored tile {"N":^15}",
    f"    {ansi.gray("_")}: unmineable tile {"ᐃ":^15}",
    f"    {ansi.red("#")}: caved in tile   {"W ᐊ ✪ ᐅ E":^15}",
    f"    {ansi.blue("P")}: player          {"ᐁ":^15}",
    f"    {ansi.green("O")}: mineral tile    {"S":^15}",
    f"    {ansi.cyan("E")}: exit/escape tile",
    f"    {ansi.yellow("M")}: monster infested tile",
    f"    {ansi.purple("D")}: monster den tile",
    f"    {ansi.graybgrd(" ") + ansi.reset()}: tile has item"]
# refer to Tile.py, in @override to see comments for each symbol's color, main.py showMap for P

mapWidth = 25 # must be greater than 5
mapHeight = 25 # must be greater than 5

def game_objective():
    print(f"{ansi.blue("You are an aspiring dwarf")} native to the Great Northern Mountains, being born\n"
    f'and raised in “Zwergberg”, the dwarven village {ansi.blue("located in the most Northern part")}\n'
    "of the mine. Recently coming of age, you are ready to put your pickaxe to use\n"
    f"and {ansi.green("strike it rich!")} But strange rumors have been beginning to surface that the\n"
    "mountain’s caverns and crevices, which have been safely mined safely for\n"
    f"innumerable generations, are destined to {ansi.red("COLLAPSE!")} Strange tremors have been\n"
    f"occurring more frequently, causing parts of the mine to {ansi.red("cave in")}, and the {ansi.yellow("mine's")}\n"
    f"{ansi.yellow("creatures")}, the flesh and stone eating {ansi.yellow("Maulwurf")}, have been increasingly active. You\n"
    f"have decided to {ansi.cyan("head South to escape")} the mine to the sky plane before it is too\n"
    f"late! Of course stuffing your pockets full of {ansi.green("valuable minerals")} on the way out.\n")

def game_rules():
    print(f"{ansi.blue(f"Every turn the player gets {NumPlayerMoves} major actions")}, but use them wisely! After each turn there\n"
          f"is a chance for a {ansi.red("disastrous event")} to occur: either a tile will {ansi.red("cave in")} or the {ansi.yellow("Maulwurf")}\n"
          f"will migrate from their {ansi.purple("dens")}. These will only become {ansi.yellow("more and more likely, and numerous,")}\n"
          f"{ansi.yellow("as the days pass by")}. It is imperative to {ansi.cyan("escape")} before you are inevitably {ansi.red("trapped")} and have\n"
          f"to wait to {ansi.red("die")}.... However, {ansi.blue("items")} can be used to clear {ansi.red("cave ins")} and eliminate {ansi.yellow("Maulwurf")}\n"
          f"from tiles, as well as {ansi.blue("reveal surrounding tiles")}. So make sure to {ansi.blue("grab them when you can!")}\n"
          f"But be strategic with what you carry though; {ansi.blue(f"you can only hold {ItemLimit} items in your inventory")}\n"
          f"at any given time. Before you {ansi.cyan("leave the mines")} it is important to {ansi.green("amass a healthy fortune")}\n"
          f"and {ansi.blue("improve your game score")}. {ansi.green("Coal")} and {ansi.green("copper")} (besides those pesky {ansi.gray("worthless rocks")}) are some\n"
          f"of the least valuable minerals to mine, and hence give the {ansi.green("lowest score")}. They are also the\n"
          f"{ansi.green("most common minerals")} to find. Collecting {ansi.green("rare minerals")}, like {ansi.green("diamonds")}, give a much {ansi.green("higher")}\n"
          f"{ansi.green("score")}. {ansi.blue("Inspecting a tile is a useful way to gleam what could be on the tile")}, and whether it\n"
          f'is worth the {ansi.purple("time")} and {ansi.purple("actions")} it takes to mine. But {ansi.yellow("be warned")}, these {ansi.blue('3 "possibilities"')} given\n'
          f"{ansi.yellow("aren't always fair")}... {ansi.blue("only one")} of those {ansi.green("minerals")} listed {ansi.blue("are real")} after all, and it's probably {ansi.green("coal")}.\n"
          f"{ansi.blue("Once")} ({ansi.red("if")}) you make it to the {ansi.cyan("exit")}, input {ansi.cyan("Escape to exit the mountains")} with your {ansi.green("fortune")}!")

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
    print(ansi.italics(f"--Entry #{entry_num}--\n{ansi.italics(description_list[entry_num])}\n--Reinput to continue reading--"))
    if entry_num == 22:
        return -22
    return 1

def start_game_text():
    print(f" --- {ansi.blue(ansi.bold_to_ital("Zwerg: Trial Beneath the Stone"))} --- \n"
          f"You descend into the mine seeking {ansi.green("riches and glory")}.\n"
          f"Your goal; {ansi.cyan("reach the escape tile and survive")}. But {ansi.b_italics("survival alone earns nothing")}.\n"
          f"To be remembered, you must {ansi.green("mine precious minerals")}, "
          f"defeat {ansi.yellow("Maulwurf")} monsters, and navigate {ansi.red("collapsing tunnels")}.\n" +
          ansi.b_italics("Each action drains your energy—move, mine, and use items; so spend each wisely.\n") +
          f"Start at the top. {ansi.cyan("Escape")} at the end.\n"
          f"Between lies {ansi.red("danger")}, {ansi.green("treasure")}, and the " +
          ansi.b_italics("chance to carve your name into the history books") + ".\n"
          f" --- {ansi.blue(ansi.bold_to_ital("May Fortunes be for the Living"))} ---\n")



helpText: dict[str, str] = {
    "rules": "rules: rules, r\n" +
            "    show the rules of the game",
    "objective": "objective: objective, lore, o\n" +
                "    show the objective of the game",
    "maulwurf": "maulwurf: maulwurf, read\n" +
               "    show the description of a maulwurf.\n    enter run maulwurf or continue again to show the next line of the description",
    "move": "move: move [direction], n, s, e, w\n" +
            "    Move the player in the specified direction.\n\n"+
            "    Options:\n"+
            "        n    move the player to the north\n"+
            "        s    move the player to the south\n"+
            "        e    move the player to the east\n"+
            "        w    move the player to the west\n",
    "mine": "mine: mine, m\n" +
             "    mine the the tile that the player is on",
    "inspect": "inspect: inspect, look, l\n" +
                "    inspect the tile that the player is currently standing on.\n    Gives 3 possible minerals (guaranteed if Worthless Rock or Maulwurf Egg)",
    "map": "map: map, compass, check, c\n" +
            "    show the map of the mines",
    "grab": "grab: grab, g, pick\n"+
            "    grab the item from the tile the player is standing on.\n\n"+
            "    if there is no item on the tile, nothing will be changed.\n\n"+
            "    if there is an item on the tile and your inventory is full, you will grab the item from the tile and drop an item of a separate type.",
    "use": "use: use [index] [direction], dynamite [direction], weapon [direction], mushroom [direction]\n" +
            "    use a specified item in the specified direction.\n\n"+
            "    if the item cannot be used in the direction, nothing will happen.\n\n"+
            "    Commands that are the item name only take a direction and attempt to use the item they are named after in the specified dierection.",
    "help": "help: help [command]\n" +
            "    If run with no command input, shows most available commands.\n\n" +
            "    If run with a command input, shows the help page for that command",
    "inventory": "inventory: inventory, i\n" +
                "    Show the inventory of the player.",
    "quit": "quit: quit [game/quit/yes/y/q]\n" +
            "    quits the game if given a confirmation.",
    "save": "save: save\n" +
            "    save the game. Will prompt for a save name after running."}

commandAliases: dict[str, list[str]] = {"rules": ["r"],
                                        "objective": ["lore", "o"],
                                        "maulwurf": ["read"],
                                        "move": ["n", "s", "e", "w"],
                                        "mine": ["m"],
                                        "inspect": ["look", "l"],
                                        "map": ["map", "compass", "check", "c"],
                                        "grab": ["g", "pick"],
                                        "use": ["dynamite", "weapon", "mushroom"],
                                        "help": [],
                                        "inventory": ["i"],
                                        "quit": ["q"]}

