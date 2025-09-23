import random
from Constants import Minerals
import Constants

# rest of code goes here

class Day: #used to count the number of days that have passed
    def __init__(self):
        self.counter = 0
    def count_increase(self):
        self.counter += 1
Day = Day()

class Events: #calculates if an event has will occur based on the number of days passed
    def __init__(self):
        self.occurred_daily = 0

    def occurrence_probability(self):
        number_of_events = Constants.event_number_scaler(Day.counter) #sets number of events equal to the number off our formula
        while number_of_events > 0: #while potential events haven't occurred
            event_occurred = random.randint(1,Constants.DenominatorEventsOccur) # DEO = 6
            if event_occurred == 1: # 1/6 chance of occurring
                self.occurred_daily += 1
            number_of_events -= 1
            # TODO: insert function here that picks the event that would occur (which leads to the specific event's output)
            self.occurred_daily = 0 # placement depends on how above function operates
        # self.occurred_daily # could technically be here too
Events = Events()

def handleInput(input: str):
    global running
    command = input.split(" ")[0].lower().strip()
    arguments = input.split(" ").pop(0) # args will be passed to each command when they're implimented
    match command:
        case "start" | "s":
            # TODO: add run function when implimented
            pass
        case "move":
            # TODO: add move function when implimented
            pass
        case "mine" | "m":
            # TODO: add mine function when implimented
            pass
        case "inspect" | "i":
            # TODO: add inspect function when implimented
            pass
        case "grab" | "g":
            # TODO: add grab function when implimented
            pass
        case "dynamite" | "d":
            # TODO: add dynamite (remove caved in tile) function when implimented
            pass
        case "fight" | "f" | "battle" | "b" | "kill":
            # TODO: add fight function when implimented
            pass
        case "exit" | "e":
            running = False
        case _:
            print(f"mine game: {command}: not found.")


running = True

# game loop
while running:
    # run player moves
    for turn in range(Constants.NumPlayerMoves):
        command = input(">>> ")
        handleInput(command)

    Events.occurrence_probability()
    Day.count_increase()
    # TODO: add event generator when done

