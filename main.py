import random
from Constants import Minerals
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

def occurrence_probability(numDays: int):
    possibleEvents = Constants.event_number_scaler(numDays) #sets number of events equal to the number off our formula
    numEvents = 0
    while possibleEvents > 0: #while potential events haven't occurred
        event_occurred = random.randint(1,Constants.DenominatorEventsOccur) # DEO = 6
        if event_occurred == 1: # 1/6 chance of occurring
            numEvents += 1
        possibleEvents -= 1
        # TODO: insert function here that picks the event that would occur (which leads to the specific event's output)


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
                line += "\033[36mP\033[0m " # makes P (the player) cyan
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
          "Help                 Quit (game, quit)")


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
            case "s" | "south":
                newPos = (player.pos[0] + 0, player.pos[1] + 1)
            case "e" | "east":
                newPos = (player.pos[0] + 1, player.pos[1] + 0)
            case "w" | "west":
                newPos = (player.pos[0] - 1, player.pos[1] + 0)
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
                print(f"moved {arg}")
        else:
            print("cannot move that direction")
    else:
        print(f"move: unknown argument \"{arg}\". Valid arguments include n, s, e, w, north, south, east, or west")



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
    # TODO: add event generator when done

