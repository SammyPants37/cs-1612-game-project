import random
from Constants import Minerals
import Constants
import Tile, Player

# rest of code goes here


class Events: #calculates if an event has will occur based on the number of days passed
    def __init__(self):
        self.occurred_daily = 0

    def occurrence_probability(self, numDays: int):
        number_of_events = Constants.event_number_scaler(numDays) #sets number of events equal to the number off our formula
        while number_of_events > 0: #while potential events haven't occurred
            event_occurred = random.randint(1,Constants.DenominatorEventsOccur) # DEO = 6
            if event_occurred == 1: # 1/6 chance of occurring
                self.occurred_daily += 1
            number_of_events -= 1
            # TODO: insert function here that picks the event that would occur (which leads to the specific event's output)
            self.occurred_daily = 0 # placement depends on how above function operates
        # self.occurred_daily # could technically be here too
events = Events()


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
    player = Player.Player((playerX, 0))
    return map


def handleInput(input: str):
    global running
    command = input.split(" ")[0].lower().strip()
    arguments = input.split(" ").pop(0) # args will be passed to each command when they're implemented
    match command:
        case "rules" | "r":
            # TODO: add rules function when implemented
            pass
        case "objective" | "lore" | "o" | "l":
            # TODO: add objective defining function when implemented
            pass
        case "move":
            # TODO: add move function when implemented, make sure to include the cardinal directions
            pass
        case "mine" | "m":
            # TODO: add mine function when implemented
            pass
        case "inspect" | "i":
            # TODO: add inspect function when implemented
            pass
        case "compass" | "map" | "check" | "c":
            # TODO: add map and compass function when implemented
            pass
        case "grab" | "pick" | "g" | "p":
            # TODO: add grab function when implemented
            pass
        case "dynamite" | "d":
            # TODO: add dynamite (remove caved in tile) function when implemented
            pass
        case "weapon" | "fight" | "f" | "battle" | "b" | "kill":
            # TODO: add fight function when implemented
            pass
        case "quit" | "q":
            # TODO: make a confirmation for quitting the game
            running = False
        case _:
            print(f"mine game: {command}: not found.")


# beginning of game code
daysPassed = 0
player: Player.Player
map = generateMap()
running = True


# game loop
while running:
    # run player moves
    for turn in range(Constants.NumPlayerMoves):
        command = input(">>> ")
        handleInput(command)

    events.occurrence_probability(daysPassed)
    daysPassed += 1
    # TODO: add event generator when done

