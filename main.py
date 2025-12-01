import random, json
from Constants import Minerals, mapHeight, mapWidth, ItemLimit
import Constants, Tile, Player

# rest of code goes here

def reload_or_start_new() -> tuple[int, Player.Player, list[list[Tile.Tile]]]: # leaving as skeleton, might want to incorporate into quit input (or its own)
    answer = input("What game would you like to load? (New Game or Load Game)\n>>> ").strip().lower()
    if answer in ("n", "new game", "new"):
        print("Input accepted\n")
        player = Player.Player()
        return 0, player, generateMap(player)
    elif answer in ("l", "load game", "load", "save", "saved file", "reload", "reload file"):
        try:
            player = Player.Player()
            map: list[list[Tile.Tile]] = []
            daysPassed = 0
            fileName = input("what save file would you like to open?")
            with open(fileName+".json", "r") as file:
                reader = json.load(file)
                daysPassed = reader["daysPassed"]
                player.total_score = reader["player"]["total_score"]
                player.items = [Constants.Items(item) for item in reader["player"]["items"]]
                player.minerals_in_bag = [Minerals.mineralTypes[mineral] for mineral in reader["player"]["minerals_in_bag"]]
                player.pos = (reader["player"]["pos"][0], reader["player"]["pos"][1])
                player.actions_left = reader["player"]["actions_left"]
                rowIndex, colIndex = 0, 0
                for row in reader["map"]:
                    # print(row)
                    map.append([])
                    colIndex = 0
                    for item in row:
                        map[rowIndex].append(Tile.Tile(
                                                            (item["pos"][0], item["pos"][1]),
                                                            Minerals.mineralTypes[item["resourceType"]],
                                                            item["isExit"],
                                                            [Minerals.mineralTypes[mineral] for mineral in item["fake_types"]]))
                        map[rowIndex][colIndex].cavedIn = item["isCavedIn"]
                        map[rowIndex][colIndex].isDiscovered = item["isDiscovered"]
                        map[rowIndex][colIndex].hasMaulwurf = item["hasMaulwurf"]
                        map[rowIndex][colIndex].setItem(Constants.Items(item["item"]))
                        colIndex += 1
                    rowIndex += 1
            return daysPassed, player, map
        except FileNotFoundError:
            print("invalid file. Please input a valid file in the same directory as the program.")
            return reload_or_start_new()
        print("something has gone wrong")
        return reload_or_start_new()
    else:
        print('(Please input either "New" or "Load")')
        return reload_or_start_new()

def save_game(map: list[list[Tile.Tile]], player: Player.Player, daysPassed: int):
    save = {}
    save["player"] = {
        "total_score": player.total_score,
        "items":[i.value for i in player.items],
        "minerals_in_bag": [i.name for i in player.minerals_in_bag],
        "pos":player.pos,
        "actions_left":player.actions_left}
    save["daysPassed"] = daysPassed
    save["map"] = []
    rowIndex = 0
    for row in map:
        save["map"].append([])
        for item in row:
            save["map"][rowIndex].append({    "pos":item.pos,
                                         "resourceType":item.resourceType.name,
                                         "fake_types": [i.name for i in item.fakeTypes],
                                         "isCavedIn":item.cavedIn,
                                         "isDiscovered":item.isDiscovered,
                                         "isExit":item.isExit,
                                         "hasMaulwurf":item.hasMaulwurf,
                                         "item": item.item.value})
        rowIndex += 1
    fileName = input("what do you want to name your save?")
    with open(fileName+".json", "w") as file:
        json.dump(save, file, indent=4, sort_keys=False)

def play_again():
    answer = input("\nWould you like to play again? (Yes or No): ").strip().lower()
    if answer == "yes" or answer == "y":
        return True
    else:
        print("Thank you for playing Zwerg. Goodbye!")
        return False

def drop_item(tilePos: tuple[int, int]):
    # grab_item takes the player's tile's item, spits out whatever will have to be dropped
    dropped_item: Constants.Items = player.grab_item(map[tilePos[1]][tilePos[0]].item)
    map[tilePos[1]][tilePos[0]].setItem(dropped_item) # sets the tile to the dropped item (sometimes nothing)

def useItem(args: list[str], player: Player.Player):
    itemIndex = args[0]

    if itemIndex.isdigit():
        itemIndex = int(itemIndex) - 1
    else:
        print(ansi.b_italics("please input a number as the first argument to specify the item to use"))
        return

    if itemIndex < 0 or itemIndex > ItemLimit - 1:
        print(ansi.b_italics("first argument needs to be within "
                             f"{ansi.bold_to_ital("1")} and {ansi.bold_to_ital(ItemLimit)}"))
        return

    item = player.items[itemIndex]

    if item == Constants.Items.mushroom:
        use_mushroom(map, player.pos)
        player.items[itemIndex] = Constants.Items.nothing
        player.actions_left -= 2
        return

    if len(args) > 1:
        direction = args[1]
    else:
        print(ansi.b_italics(f"missing argument for {ansi.bold_to_ital("direction")} to use the item."))
        return


    itemUsable: bool = False

    match direction:
        case "n" | "north":
            if player.pos[1] > 0:
                if map[player.pos[1] - 1][player.pos[0]].is_usable(item):
                    if item == Constants.Items.dynamite:
                        map[player.pos[1] - 1][player.pos[0]].setCavedIn(False)
                    elif item == Constants.Items.weapon:
                        map[player.pos[1] - 1][player.pos[0]].setMaulwurfStatus(False)
                    itemUsable = True
        case "s" | "south":
            if player.pos[1] < mapHeight - 1:
                if map[player.pos[1] + 1][player.pos[0]].is_usable(item):
                    if item == Constants.Items.dynamite:
                        map[player.pos[1] + 1][player.pos[0]].setCavedIn(False)
                    elif item == Constants.Items.weapon:
                        map[player.pos[1] + 1][player.pos[0]].setMaulwurfStatus(False)
                    itemUsable = True
        case "e" | "east":
            if player.pos[0] < mapWidth - 1:
                if map[player.pos[1]][player.pos[0] + 1].is_usable(item):
                    if item == Constants.Items.dynamite:
                        map[player.pos[1]][player.pos[0] + 1].setCavedIn(False)
                    elif item == Constants.Items.weapon:
                        map[player.pos[1]][player.pos[0] + 1].setMaulwurfStatus(False)
                    itemUsable = True
        case "w" | "west":
            if player.pos[0] > 0:
                if map[player.pos[1]][player.pos[0] - 1].is_usable(item):
                    if item == Constants.Items.dynamite:
                        map[player.pos[1]][player.pos[0] - 1].setCavedIn(False)
                    elif item == Constants.Items.weapon:
                        map[player.pos[1]][player.pos[0] - 1].setMaulwurfStatus(False)
                    itemUsable = True
        case _:
            print(ansi.b_italics("Please input a valid direction. Valid directions include "
                                 f"{ansi.bold_to_ital("north")}, {ansi.bold_to_ital("south")}, "
                                 f"{ansi.bold_to_ital(")east")}, and {ansi.bold_to_ital("west")}."))

    if itemUsable:
        if item.name == "weapon": maulwurf_remains(Minerals.mineralTypes.maulwurf)
        print(ansi.b_italics(f"Used {item.name},"), end=" ")
        player.items[itemIndex] = Constants.Items.nothing
        player.actions_left -= 1
        move([direction], map, player)
    else:
        print(ansi.b_italics("Item is not usable in that direction."))

def maulwurf_remains(monster: Minerals.mineralTypes):
    player.add_score(monster)
    print(ansi.italics(monster.miningDescription))
    print(f"{ansi.b_italics("Gathered Resource")}: {ansi.g_bold(monster.description)} ({ansi.g_bold(f"+{monster.score_value:,}!")}) --> {ansi.cyan(f"Current Score: {player.total_score:,}")}")

def use_mushroom(map: list[list[Tile.Tile]], pos: tuple[int, int]) -> None: # skeleton based off of mini map
    print(ansi.italics("As the psilocybe slips down your gullet, you feel a heightened connection to the caverns around you"),
          f"\n{ansi.b_italics("Used mushroom")}")
    print("-----mini map-----")
    if pos[1] in (range(3)):  # defines which rows will be shown on the mini map based off player.pos
        row_bounds = (0, 5)  # first case is for when the player is near the top of the map
    elif pos[1] in (range((mapHeight - 3), mapHeight)):  # then when the player is near the bottom
        row_bounds = ((mapHeight - 5), mapHeight)
    else:  # lastly, all in between positions are defined directly from player.pos
        row_bounds = ((pos[1] - 2), (pos[1] + 3))
    if pos[0] in (range(3)):  # defines which item will be shown on the mini map based off player.pos (similar way to row)
        item_bounds = (0, 5)
    elif pos[0] in (range((mapWidth - 3), mapWidth)):
        item_bounds = ((mapWidth - 5), mapWidth)
    else:
        item_bounds = ((pos[0] - 2), (pos[0] + 3))
    for row in map[row_bounds[0]:row_bounds[1]]:
        line = "    "
        for item in row[item_bounds[0]:item_bounds[1]]:  # mimics what I did for row
            item.make_discovered()
            if item.pos == player.pos:
                line += ansi.blue("P ")  # makes P (the player) blue
            else:
                line += str(item) + " "
        print(line)
    print("------------------")

def mineTile(tilePos: tuple[int, int]):
    tileMineral: Minerals.mineralTypes = map[tilePos[1]][tilePos[0]].resourceType
    player.add_score(tileMineral)
    map[tilePos[1]][tilePos[0]].drainMineral()
    print(ansi.italics(tileMineral.miningDescription))
    print(f"{ansi.b_italics("Mined Mineral")}: {ansi.italics(ansi.green(tileMineral.description))} "
          f"({ansi.g_bold(f"+{tileMineral.score_value:,}!")}) --> {ansi.cyan(f"Current Score: {player.total_score:,}")}")

def inspect_tile(tilePos: tuple[int, int]):
    true_mineral = map[tilePos[1]][tilePos[0]].resourceType  #gives the real mineral
    fake_mineral = map[tilePos[1]][tilePos[0]].fakeTypes # gives 2 fake minerals for the tile the player is on
    true_mineral_pos = random.randint(1, 3)
    # randomly generates a position for the real mineral every inspect, keeps order
    if true_mineral_pos == 1:
        said_mineral = [true_mineral, fake_mineral[0], fake_mineral[1]]
    elif true_mineral_pos == 2:
        said_mineral = [fake_mineral[1], true_mineral, fake_mineral[0]]
    else:  # when true_mineral_pos is the 3rd position
        said_mineral = [fake_mineral[0], fake_mineral[1], true_mineral]
    print(f"Hmm... I think I could find {ansi.g_bold(said_mineral[0].description)}, "
                                      f"{ansi.g_bold(said_mineral[1].description)}, or "
                                      f"{ansi.g_bold(said_mineral[2].description)} in this segment of the mine")

    if map[tilePos[1]][tilePos[0]].item != map[tilePos[1]][tilePos[0]].item.nothing: #if there is an item on the player's tile
        print("While gleaming the mine for potential minerals, I found a "
              f"{ansi.b_bold(map[tilePos[1]][tilePos[0]].item.name)} that I could grab if space allows")

def check_pos(player: Player.Player): # didn't want player.pos in Tile.py
    global running
    if map[player.pos[1]][player.pos[0]].isExit: # if the player is on the exit
        answer = input(f"{ansi.cyan("Do you want to escape the mountains?")} "
                       f"({ansi.blue("Yes")} or {ansi.blue("No")}): ").strip().lower()
        if answer in ("yes", "y", "escape", "exit"):
            player.exit_message(z_calendar)
            running = False
            player.actions_left = 0
        elif answer in ("no", "n", "nope", "nada", "stay"):
            print(ansi.italics("You decide to continue mining... hopefully your greed doesn't get the best of you"))
        else:
            print(f'Please input a valid answer. Enter "{ansi.cyan("Exit")}" to try again')
    elif map[player.pos[1]][player.pos[0]].hasMaulwurf or map[player.pos[1]][player.pos[0]].cavedIn: #checks if the tile is valid
        if map[player.pos[1]][player.pos[0]].cavedIn: # gives feedback if it is caved in
            print(f"Ow! The cavern you are in {ansi.red("collapsed!")}")
        elif map[player.pos[1]][player.pos[0]].hasMaulwurf: # if it is not caved in, gives feedback that there are Maulwurf
            print(f"Oh no! An overwhelming horde of {ansi.yellow("Maulwurf")} flooded into the cave!")

        available_directions = []  # below checks to see if a given direction is valid, appending it if it is
        if player.pos[1] - 1 >= 0 and not (map[player.pos[1] - 1][player.pos[0]].cavedIn or map[player.pos[1] - 1][player.pos[0]].hasMaulwurf):
            available_directions.append("n")
        if player.pos[1] + 1 < mapHeight and not (map[player.pos[1] + 1][player.pos[0]].cavedIn or map[player.pos[1] + 1][player.pos[0]].hasMaulwurf):
            available_directions.append("s")
        if player.pos[0] + 1 < mapWidth and not (map[player.pos[1]][player.pos[0] + 1].cavedIn or map[player.pos[1]][player.pos[0] + 1].hasMaulwurf):
            available_directions.append("e")
        if player.pos[1] - 1 >= 0 and not (map[player.pos[1]][player.pos[0] - 1].cavedIn or map[player.pos[1]][player.pos[0] - 1].hasMaulwurf):
            available_directions.append("w")
        if len(available_directions) == 0: # if there are no valid directions
            running = False
            player.actions_left = 0
            print(ansi.red("YOU DIED") + f" -- {ansi.cyan("Score: 0")}"
                                         f"\n{ansi.italics("Thank you for playing Zwerg: Trial Beneath the Stone")}")
        else:
            move(random.choice(available_directions), map, player) # else a random direction is picked to move

def occurrence_probability(numDays: int):
    possibleEvents = Constants.event_number_scaler(numDays) #sets number of events equal to the number off our formula
    while possibleEvents > 0: #while potential events haven't occurred
        event_occurred = random.randint(1,Constants.DenominatorEventsOccur) # DEO = 6
        if event_occurred == 1: # 1/6 chance of occurring
            rand_event = random.choices(("infest", "cave in"), weights = Constants.event_weights)[0]
            if rand_event == "infest":
                rand_den_infest()
            else:
                rand_cave_in()
        possibleEvents -= 1

def rand_cave_in():
    unblocked_tiles = []
    for h in range(mapHeight):
        for w in range(mapWidth):
            if not map[h][w].cavedIn:
                unblocked_tiles.append([w, h])
    if len(unblocked_tiles) == 0:
        return # the player will be dead afterwards, so just in case the rare error I had occurs again
    chosen_tile = random.choice(unblocked_tiles) # chooses an unblocked tile for a cave in to occur
    map[chosen_tile[1]][chosen_tile[0]].setCavedIn(True)

def rand_den_infest():
    maulwurf_dens = []
    for h in range(mapHeight):
        for w in range(mapWidth):
            if map[h][w].resourceType == Minerals.mineralTypes.monsterDen and not map[h][w].cavedIn:
                maulwurf_dens.append([w, h])
    if len(maulwurf_dens) > 0: # when there are unblocked dens
        chosen_den = random.choice(maulwurf_dens) #choose one out of them to infest from
        if not map[chosen_den[1]][chosen_den[0]].hasMaulwurf:  # if the den doesn't have Maulwurf on it
            map[chosen_den[1]][chosen_den[0]].setMaulwurfStatus(True)  # it does now
        else: # else when it has Maulwurf
            tries_left = mapWidth # I chose mapWidth (which scales good enough) as the cap for looking for values
            infest_tile(chosen_den, tries_left) # I thought recursion was a more appropriate looping mechanism
    else:
        rand_cave_in() #when all the dens are blocked a cave in happens randomly instead

def infest_tile(tilePos: tuple[int, int], tries_left: int):
        available_directions = [] # below checks to see if a given direction is valid, appending it if it is
        if tilePos[1] - 1 >= 0 and not map[tilePos[1] - 1][tilePos[0]].cavedIn:
            available_directions.append("north")
        if tilePos[1] + 1 < mapHeight and not map[tilePos[1] + 1][tilePos[0]].cavedIn:
            available_directions.append("south")
        if tilePos[0] + 1 < mapWidth and not map[tilePos[1]][tilePos[0] + 1].cavedIn:
            available_directions.append("east")
        if tilePos[0] - 1 >= 0 and not map[tilePos[1]][tilePos[0] - 1].cavedIn:
            available_directions.append("west")

        if tries_left == 0 or len(available_directions) == 0: # if cap is reached, or there's no valid direction
            map[tilePos[1]][tilePos[0]].setCavedIn(True) # tile caves in
            return

        infest_direction = random.choice(available_directions) # randomly selects direction out of valid ones
        if infest_direction == "north":
            if map[tilePos[1] - 1][tilePos[0]].hasMaulwurf: # if the tile already has Maulwurf
                infest_tile((tilePos[0], tilePos[1] - 1), tries_left - 1) # we now infest that tile
            else: # if it doesn't have Maulwurf
                map[tilePos[1] - 1][tilePos[0]].setMaulwurfStatus(True) # now it does
        elif infest_direction == "south":
            if map[tilePos[1] + 1][tilePos[0]].hasMaulwurf: # if the tile already has Maulwurf
                infest_tile((tilePos[0], tilePos[1] + 1), tries_left - 1) # we now infest that tile
            else: # if it doesn't have Maulwurf
                map[tilePos[1] + 1][tilePos[0]].setMaulwurfStatus(True) # now it does
        elif infest_direction == "east":
            if map[tilePos[1]][tilePos[0] + 1].hasMaulwurf: # if the tile already has Maulwurf
                infest_tile((tilePos[0] + 1, tilePos[1]), tries_left - 1) # we now infest that tile
            else: # if it doesn't have Maulwurf
                map[tilePos[1]][tilePos[0] + 1].setMaulwurfStatus(True) # now it does
        else: # for when the direction is "west"
            if map[tilePos[1]][tilePos[0] - 1].hasMaulwurf: # if the tile already has Maulwurf
                infest_tile((tilePos[0] - 1, tilePos[1]), tries_left - 1) # we now infest that tile
            else: # if it doesn't have Maulwurf
                map[tilePos[1]][tilePos[0] - 1].setMaulwurfStatus(True) # now it does

def generateMap(player: Player.Player) -> list[list[Tile.Tile]]:
    map:list[list[Tile.Tile]] = []
    for h in range(Constants.mapHeight):
        map.append([])
        for w in range(Constants.mapWidth):
            map[h].append(Tile.Tile((w, h), Tile.mineralRandomizer(1)[0],False, Tile.mineralRandomizer(2)))
            map[h][w].setItem(random.choices(list(Constants.Items), weights = Constants.item_weights())[0])
    map[Constants.mapHeight-1][random.randint(0, Constants.mapWidth-1)].isExit = True
    playerX = random.randint(0, Constants.mapWidth-1)
    player.setPos((playerX, 0))
    map[0][playerX].isDiscovered = True
    return map

def showMap(map: list[list[Tile.Tile]], playerPos: tuple[int, int]) -> None:
    workingRow = 0
    for row in map:
        line = ""
        for item in row:
            if item.pos == playerPos:
                line += ansi.blue("P ") # makes P (the player) blue
            else:
                line += str(item) + " "
        if workingRow  < len(Constants.mapExtras):
            line += Constants.mapExtras[workingRow]
        print(line)
        workingRow += 1

def show_mini_map(map: list[list[Tile.Tile]], pos: tuple[int, int]) -> None: # skeleton based off of showMap function
    print("-----mini map-----")
    if pos[1] in (range(3)): # defines which rows will be shown on the mini map based off player.pos
        row_bounds = (0, 5) # first case is for when the player is near the top of the map
    elif pos[1] in (range((mapHeight - 3), mapHeight)): # then when the player is near the bottom
        row_bounds = ((mapHeight - 5), mapHeight)
    else: # lastly, all in between positions are defined directly from player.pos
        row_bounds = ((pos[1] - 2), (pos[1] + 3))
    if pos[0] in (range(3)): # defines which item will be shown on the mini map based off player.pos (similar way to row)
        item_bounds = (0, 5)
    elif pos[0] in (range((mapWidth - 3), mapWidth)):
        item_bounds = ((mapWidth - 5), mapWidth)
    else:
        item_bounds = ((pos[0] - 2), (pos[0] + 3))
    for row in map[row_bounds[0]:row_bounds[1]]:
        line = "    "
        for item in row[item_bounds[0]:item_bounds[1]]: # mimics what I did for row
            if item.pos == pos:
                line += ansi.blue("P ") # makes P (the player) blue
            else:
                line += str(item) + " "
        print(line)
    print("------------------")

def helpMenu(args: list[str]):
    if args[0] == "": # show the main help menu if no arguement is supplied
        alignmentString = "{:<15s} {:<20s} {:<10s}"
        print(ansi.italics("Welcome to the game! Here are some inputs you can use"))
        print(ansi.italics(alignmentString.format("Rules", "Move (n, s, e, w)", "Grab") + "\n" +
              alignmentString.format("Objective", "Mine", "Use (dynamite, weapon, mushroom)" + "\n" +
              alignmentString.format("Map", "Inspect", "Inventory") + "\n" +
              alignmentString.format("Help (command)", "Quit (game, quit)", "save"))))
    else:
        if args[0] in Constants.helpText:
            print(ansi.italics(Constants.helpText[args[0]]))
        else:
            for command in Constants.commandAliases: # wish I didn't have to iterate over the aliases but its the best solution at the moment
                for item in Constants.commandAliases[command]:
                    if args[0] == item:
                       print(ansi.italics(Constants.helpText[command]))
                       return
            print(ansi.italics(f"no such help page. Help pages include: {", ".join(Constants.helpText.keys())}"))

def move(args: list[str], map: list[list[Tile.Tile]], player: Player.Player):
    arg = args[0]
    if len(args) > 1:
        print(ansi.italics("all arguments past the first one have been discarded"))
    newPos: tuple[int, int] = (0, 0)
    match arg:
        case "n" | "north":
            newPos = (player.pos[0] + 0, player.pos[1] - 1)
            arg = "North"
        case "s" | "south":
            newPos = (player.pos[0] + 0, player.pos[1] + 1)
            arg = "South"
        case "e" | "east":
            newPos = (player.pos[0] + 1, player.pos[1] + 0)
            arg = "East"
        case "w" | "west":
            newPos = (player.pos[0] - 1, player.pos[1] + 0)
            arg = "West"
        case _:
            print(ansi.b_italics(f"move: unknown argument \"{arg}\". "
                                 "Valid arguments include n, s, e, w, north, south, east, or west"))
            return

    YCordValid: bool = newPos[1] >= 0 and newPos[1] < Constants.mapHeight
    XCordValid: bool = newPos[0] >= 0 and newPos[0] < Constants.mapWidth
    if YCordValid and XCordValid:
        map[newPos[1]][newPos[0]].isDiscovered = True #makes it so the tile is discovered if the coords are valid
        # happens regardless if the tile is cavedIn or hasMaulwurf, makes so they will show up on map
        if map[newPos[1]][newPos[0]].cavedIn:
            #tells the player if the tile has caved in, makes it show on map, hints at dynamite
            print(f"It seems the cave has {ansi.red("caved in")} that way... "
                  f"{ansi.b_bold("dynamite")} would be useful here")
        elif map[newPos[1]][newPos[0]].hasMaulwurf:
            #tells the player if the tile has Maulwurf, makes it show on map, hints at weapon
            print(f"Terrible {ansi.yellow("growling")} rings through the cavern that way, "
                  f"alongside a waft of blood... only a {ansi.b_bold("weapon")} would allow continuation")
        else:
            player.pos = newPos #sets the player's position to the new one
            player.actions_left -= 1 #takes away an action after the player has successfully moved
            print(ansi.b_italics(f"Moved {arg}"))
            inspect_tile(newPos)
    else:
            print(ansi.italics("cannot move that direction"))

def showInventory():
    for i in range(len(player.items)):
        print(f"{i+1}: {player.items[i].name}")

def handleInput(input: str, player: Player.Player, map: list[list[Tile.Tile]]):
    global running, user_quit
    command = input.split(" ")[0].lower().strip()
    arguments = input.split(" ")[1:] # args will be passed to each command when they're implemented
    arguments = [arg.lower().strip() for arg in arguments]
    if len(arguments) == 0:
        arguments.append("")
    match command:
        case "rules" | "r":
            Constants.game_rules()
        case "objective" | "lore" | "o":
            Constants.game_objective()
        case "maulwurf" | "read" | "continue":
            Constants.entry_counter += Constants.maulwurf_description(Constants.entry_counter)
        case "move":
            move(arguments, map, player)
            show_mini_map(map, player.pos)
        case "n" | "s" | "e" | "w" | "north" | "south" | "east" | "west":
            move(list(command), map, player)
            print(player.pos)
            show_mini_map(map, player.pos)
        case "mine" | "m":
            player.actions_left -= 1
            mineTile(player.pos)
        case "inspect" | "l" | "look":
            inspect_tile(player.pos)
        case "compass" | "map" | "check" | "c":
            showMap(map, player.pos)
        case "grab" | "pick" | "g":
            drop_item(player.pos)
        case "dynamite" | "d":
            try:
                itemIndex = player.items.index(Constants.Items.dynamite)
                arguments.insert(0, str(itemIndex + 1))
                useItem(arguments, player)
            except ValueError:
                print(ansi.b_italics("no dynamite in inventory"))
        case "weapon" | "fight" | "f" | "battle" | "b" | "kill":
            try:
                itemIndex = player.items.index(Constants.Items.weapon)
                arguments.insert(0, str(itemIndex + 1))
                useItem(arguments, player)
            except ValueError:
                print(ansi.b_italics("no weapon in inventory"))
        case "mushroom" | "shroom" | "psilocybe" | "conecsiemuer" | "p":
            try:
                itemIndex = player.items.index(Constants.Items.mushroom)
                arguments.insert(0, str(itemIndex + 1))
                useItem(arguments, player)
            except ValueError:
                print(ansi.b_italics("no mushroom in inventory"))
        case "use":
            useItem(arguments, player)
        case "help":
            # show the help menu when the help command is run
            helpMenu(arguments)
        case "inventory" | "i":
            showInventory()
        case "quit" | "q":
            if not set(arguments).isdisjoint(["quit", "yes", "y", "q", "game"]):
                print("Thank you for playing Zwerg. Goodbye!")
                running = False
                player.actions_left = 0
                user_quit = True
            else:
                print("Are you sure you would like to quit? Progress will not be saved...\n(Please type in Quit Game to confirm).")
        case "z": # got sick of spamming mine
            if Constants.devMode:
                player.actions_left -= 12
        case "save":
            save_game(map, player, daysPassed)
        case _:
            print(ansi.b_italics(f"mine game: {ansi.bold_to_ital(command)}: not found."))


# beginning of game code
Constants.start_game_text()


while True:
    daysPassed = 0
    player: Player.Player = Player.Player()
    ansi: Constants.AnsiColors = Constants.AnsiColors()
    map = generateMap(player)
    running = True
    user_quit = False

    daysPassed, player, map = reload_or_start_new()
    # reload_or_start_new() # TODO: uncomment after completing menu
    helpMenu([""])

    # game loop
    while running:
        player.actions_left += Constants.NumPlayerMoves #refunds 3 actions
        # run player moves
        while player.actions_left > 0:
            check_pos(player) # checks if Maulwurf or CaveIn occurred on the player's tile, kicking them to a new tile if so
            if player.actions_left == 0: break
            command = input(">>> ")
            handleInput(command, player, map)
        if running:
            occurrence_probability(daysPassed)
            daysPassed += 1
            z_calendar = Constants.zwerg_calendar_system(daysPassed)
            # z_calendar = [day_of_week, week, month, day_of_month, month_name, year, weekday_num]
            print(ansi.italics(f"\n{ansi.cyan(f"Week {z_calendar[1]}")}") + ansi.italics(f": {z_calendar[0]}, {ansi.cyan(f"Day {z_calendar[3]}")} ") +
                           ansi.italics(f"of {z_calendar[4]} ({ansi.cyan(f"{z_calendar[2]}/{z_calendar[3]}/{z_calendar[5]}")}" + ansi.italics(")")))
            print(ansi.italics("As you go to sleep for the evening, you hear the rumbles of change in the mines"))

    # After game ends, ask if player wants to play again (unless user quit)
    if user_quit:
        break
    if not play_again():
        break

