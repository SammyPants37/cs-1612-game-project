import random
from Constants import Minerals
import Constants, Tile, Player

# rest of code goes here

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
            map[h].append(Tile.Tile((w, h), random.choices(list(Minerals.mineralTypes), weights=Minerals.weights)[0], False))
            map[h][w].setItem(random.choices(list(Constants.Items), weights=[290, 5, 5])[0])
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
                line += "P "
            else:
                line += str(item) + " "
        if workingRow  < len(Constants.mapExtras):
            line += Constants.mapExtras[workingRow]
        print(line)
        workingRow += 1


def helpMenu():
    print("Welcome to the game! Here are some inputs you can use")
    print("Rules")
    print("Objective")
    print("Move (n, s, e, w)")
    print("Mine")
    print("Inspect")
    print("grab")
    print("dynamite")
    print("weapon")
    print("help")
    print("Quit (game, quit)")


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
        if not map[newPos[1]][newPos[0]].cavedIn and YCordValid and XCordValid:
            player.pos = newPos
            map[newPos[1]][newPos[0]].isDiscovered = True
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
    match command:
        case "rules" | "r":
            # TODO: add rules function when implemented
            pass
        case "objective" | "lore" | "o" | "l":
            # TODO: add objective defining function when implemented
            pass
        case "move":
            player.actions_left -= 1
            move(arguments, map)
            pass
        case "mine" | "m":
            player.actions_left -= 1
            # TODO: add mine function when implemented
            pass
        case "inspect" | "i":
            # TODO: add inspect function when implemented
            pass
        case "compass" | "map" | "check" | "c":
            showMap(map)
        case "grab" | "pick" | "g" | "p":
            # TODO: add grab function when implemented
            pass
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

    occurrence_probability(daysPassed)
    daysPassed += 1
    # TODO: add event generator when done

