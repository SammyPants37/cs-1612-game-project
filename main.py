import random
from Constants import Minerals, mapHeight, mapWidth
import Constants, Tile, Player

# rest of code goes here

def drop_item(tilePos: tuple[int, int]):
    # grab_item takes the player's tile's item, spits out whatever will have to be dropped
    dropped_item: Constants.Items = player.grab_item(map[tilePos[1]][tilePos[0]].item)
    map[tilePos[1]][tilePos[0]].setItem(dropped_item) # sets the tile to the dropped item (sometimes nothing)

def mineTile(tilePos: tuple[int, int]):
    tileMineral: Minerals.mineralTypes = map[tilePos[1]][tilePos[0]].resourceType
    player.add_score(tileMineral)
    map[tilePos[1]][tilePos[0]].drainMineral()
    print(tileMineral.miningDescription)


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
    print(f"Hmm... I think I could find {said_mineral[0].description}, {said_mineral[1].description}, or {said_mineral[2].description} in this segment of the mine")

    if map[tilePos[1]][tilePos[0]].item != map[tilePos[1]][tilePos[0]].item.nothing: #if there is an item on the player's tile
        print(f"While gleaming the mine for potential minerals, I found a {map[tilePos[1]][tilePos[0]].item.name} that I could grab if space allows")

def check_pos(pos: tuple[int, int]): # didn't want player.pos in Tile.py
    if map[pos[1]][pos[0]].hasMaulwurf or map[pos[1]][pos[0]].cavedIn: #checks if the tile is valid
        if map[pos[1]][pos[0]].cavedIn: # gives feedback if it is caved in
            print("Ow! The cavern you are in collapsed!")
        elif map[pos[1]][pos[0]].hasMaulwurf: # if it is not caved in, gives feedback that there are Maulwurf
            print("Oh no! An overwhelming horde of Maulwurf flooded into the cave!")

        available_directions = []  # below checks to see if a given direction is valid, appending it if it is
        if pos[1] - 1 >= 0 and not (map[pos[1] - 1][pos[0]].cavedIn or map[pos[1] - 1][pos[0]].hasMaulwurf):
            available_directions.append("n")
        if pos[1] + 1 < mapHeight and not (map[pos[1] + 1][pos[0]].cavedIn or map[pos[1] + 1][pos[0]].hasMaulwurf):
            available_directions.append("s")
        if pos[0] + 1 < mapWidth and not (map[pos[1]][pos[0] + 1].cavedIn or map[pos[1]][pos[0] + 1].hasMaulwurf):
            available_directions.append("e")
        if pos[1] - 1 >= 0 and not (map[pos[1]][pos[0] - 1].cavedIn or map[pos[1]][pos[0] - 1].hasMaulwurf):
            available_directions.append("w")
        if len(available_directions) == 0: # if there are no valid directions
            global running
            running = False
            player.actions_left = 0
            print("YOU DIED -- Score: 0 \nThank you for playing Maulwurf")
        else:
            move(random.choice(available_directions), map) # else a random direction is picked to move


def occurrence_probability(numDays: int):
    possibleEvents = Constants.event_number_scaler(numDays) #sets number of events equal to the number off our formula
    while possibleEvents > 0: #while potential events haven't occurred
        event_occurred = random.randint(1,Constants.DenominatorEventsOccur) # DEO = 6
        if event_occurred == 1: # 1/6 chance of occurring
            rand_event = random.randint(1, 2)
            if rand_event == 1:
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
        infest_tile(chosen_den)
    else:
        rand_cave_in() #when all the dens are blocked a cave in happens randomly instead

def infest_tile(tilePos: tuple[int, int]):
    if not map[tilePos[1]][tilePos[0]].hasMaulwurf: # if the den doesn't have Maulwurf on it
      map[tilePos[1]][tilePos[0]].setMaulwurfStatus(True) # it does now
    else: # else when it has Maulwurf (initially had a while loop, but there was a potential for an infinite loop)
        for num_tries in range(mapWidth): # I chose mapWidth (which scales good enough) as the cap for looking for values
            available_directions = [] # below checks to see if a given direction is valid, appending it if it is
            if tilePos[1] - 1 >= 0 and not map[tilePos[1] - 1][tilePos[0]].cavedIn:
                available_directions.append("north")
            if tilePos[1] + 1 < mapHeight and not map[tilePos[1] + 1][tilePos[0]].cavedIn:
                available_directions.append("south")
            if tilePos[0] + 1 < mapWidth and not map[tilePos[1]][tilePos[0] + 1].cavedIn:
                available_directions.append("east")
            if tilePos[1] - 1 >= 0 and not map[tilePos[1]][tilePos[0] - 1].cavedIn:
                available_directions.append("west")
            if num_tries == (mapWidth - 1) or len(available_directions) == 0: # if cap is reached, or there's no valid direction
                map[tilePos[1]][tilePos[0]].setCavedIn(True) # tile caves in
                break # from too much Maulwurf traffic or overcrowding, either way it caves in
            infest_direction = random.choice(available_directions) # randomly selects direction out of valid ones
            if infest_direction == "north":
                if map[tilePos[1] - 1][tilePos[0]].hasMaulwurf: # if the tile already has Maulwurf
                    tilePos = [tilePos[1] - 1, tilePos[0]] # that tile becomes the tile we are looking at, loops
                else: # if it doesn't have Maulwurf
                    map[tilePos[1] - 1][tilePos[0]].setMaulwurfStatus(True) # now it does
                    break
            elif infest_direction == "south":
                if map[tilePos[1] + 1][tilePos[0]].hasMaulwurf: # if the tile already has Maulwurf
                    tilePos = [tilePos[1] + 1, tilePos[0]] # that tile becomes the tile we are looking at, loops
                else: # if it doesn't have Maulwurf
                    map[tilePos[1] + 1][tilePos[0]].setMaulwurfStatus(True) # now it does
                    break
            elif infest_direction == "east":
                if map[tilePos[1]][tilePos[0] + 1].hasMaulwurf: # if the tile already has Maulwurf
                    tilePos = [tilePos[1], tilePos[0] + 1] # that tile becomes the tile we are looking at, loops
                else: # if it doesn't have Maulwurf
                    map[tilePos[1]][tilePos[0] + 1].setMaulwurfStatus(True) # now it does
                    break
            else: # for when the direction is "west"
                if map[tilePos[1]][tilePos[0] - 1].hasMaulwurf: # if the tile already has Maulwurf
                    tilePos = [tilePos[1], tilePos[0] - 1] # that tile becomes the tile we are looking at, loops
                else: # if it doesn't have Maulwurf
                    map[tilePos[1]][tilePos[0] - 1].setMaulwurfStatus(True) # now it does
                    break


def generateMap() -> list[list[Tile.Tile]]:
    global player
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


def showMap(map: list[list[Tile.Tile]]) -> None:
    workingRow = 0
    for row in map:
        line = ""
        for item in row:
            if item.pos == player.pos:
                line += "\033[34mP\033[0m " # makes P (the player) cyan
            else:
                line += str(item) + " "
        if workingRow  < len(Constants.mapExtras):
            line += Constants.mapExtras[workingRow]
        print(line)
        workingRow += 1


def helpMenu():
    print("Welcome to the game! Here are some inputs you can use")
    print("Rules                Move (n, s, e, w)           Grab\n"
          "Objective            Mine                        Dynamite\n"
          "Map                  Inspect                     Weapon\n"
          "Help                 Quit (game, quit)		 inventory")


def move(args: list[str], map: list[list[Tile.Tile]]):
    global player
    arg = args[0]
    if len(args) > 1:
        print("all arguments past the first one have been discarded")
    if arg in ["n", "s", "e", "w", "north", "south", "east", "west"]:
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
                newPos = player.pos

        YCordValid: bool = newPos[1] >= 0 and newPos[1] < Constants.mapHeight
        XCordValid: bool = newPos[0] >= 0 and newPos[0] < Constants.mapWidth
        if YCordValid and XCordValid:
            map[newPos[1]][newPos[0]].isDiscovered = True #makes it so the tile is discovered if the coords are valid
            # happens regardless if the tile is cavedIn or hasMaulwurf, makes so they will show up on map
            if map[newPos[1]][newPos[0]].cavedIn:
                #tells the player if the tile has caved in, makes it show on map, hints at dynamite
                print("It seems the cave has caved in that way... dynamite would be useful here")
            elif map[newPos[1]][newPos[0]].hasMaulwurf:
                #tells the player if the tile has Maulwurf, makes it show on map, hints at weapon
                print("Terrible growling rings through the cavern that way, alongside a waft of blood... only a weapon would allow continuation")
            else:
                player.pos = newPos #sets the player's position to the new one
                player.actions_left -= 1 #takes away an action after the player has successfully moved
                print(f"Moved {arg}")
        else:
            print("cannot move that direction")
    else:
        print(f"move: unknown argument \"{arg}\". Valid arguments include n, s, e, w, north, south, east, or west")


def showInventory():
    for i in range(len(player.items)):
        print(f"{i+1}: {player.items[i].name}")


def handleInput(input: str):
    global running
    command = input.split(" ")[0].lower().strip()
    arguments = input.split(" ")[1:] # args will be passed to each command when they're implemented
    arguments = [arg.lower().strip() for arg in arguments]
    if len(arguments) == 0:
        arguments.append("")
    match command:
        case "rules" | "r":
            # TODO: add rules function when implemented
            pass
        case "objective" | "lore" | "o" | "l":
            # TODO: add objective defining function when implemented
            pass
        case "move":
            move(arguments, map)
        case "n" | "s" | "e" | "w" | "north" | "south" | "east" | "west":
            move(list(command), map)
        case "mine" | "m":
            player.actions_left -= 1
            mineTile(player.pos)
        case "inspect" | "i":
            inspect_tile(player.pos)
        case "compass" | "map" | "check" | "c":
            showMap(map)
        case "grab" | "pick" | "g" | "p":
            drop_item(player.pos)
        case "dynamite" | "d":
            player.actions_left -= 2
            # TODO: add dynamite (remove caved in tile) function when implemented
            pass
        case "weapon" | "fight" | "f" | "battle" | "b" | "kill":
            player.actions_left -= 2
            # TODO: add fight function when implemented
            pass
        case "help":
            # show the help menu when the help command is run
            helpMenu()
        case "inventory":
            showInventory()
        case "quit" | "q":
            if not set(arguments).isdisjoint(["quit", "yes", "y", "q", "game"]):
                print("Thank you for playing Zwerg. Goodbye!")
                running = False
                player.actions_left = 0
            else:
                print("Are you sure you would like to quit? Progress will not be saved...\n(Please type in Quit Game to confirm).")
        case _:
            print(f"mine game: {command}: not found.")


# beginning of game code
daysPassed = 0
player: Player.Player = Player.Player()
map = generateMap()
running = True


helpMenu()

# game loop
while running:
    player.actions_left += Constants.NumPlayerMoves #refunds 3 actions
    # run player moves
    while player.actions_left > 0:
        command = input(">>> ")
        handleInput(command)

    print("as you go to sleep for the evening, you hear the rumbles of change in the mines")
    occurrence_probability(daysPassed)
    daysPassed += 1
    check_pos(player.pos) # checks if Maulwurf or CaveIn occurred on the player's tile, kicking them to a new tile if so

