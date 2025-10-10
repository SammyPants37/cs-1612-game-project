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
            


def handleInput(input: str):
    global running
    command = input.split(" ")[0].lower().strip()
    arguments = input.split(" ")[1:] # args will be passed to each command when they're implemented
    match command:
        case "rules" | "r":
            # TODO: add rules function when implemented
            pass
        case "objective" | "lore" | "o" | "l":
            # TODO: add objective defining function when implemented
            pass
        case "move":
            player.actions_left -= 1
            # TODO: add move function when implemented, make sure to include the cardinal directions
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

def menu():
    print("Welcome to the game! Here are some inputs you can use")
    print("1. Rules")
    print("2. Objective")
    print("3. Move (n, s, e, w)")
    print("4. Mine")
    print("5. Inspect")
    print("6. Inspect")
    print("7. Quit")
print(menu())

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

