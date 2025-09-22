import random
from Constants import Minerals
import Constants

# rest of code goes here

def handleInput(input: str):
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
            # TODO: add quit function when implimented
            pass
        case _:
            print(f"mine game: {command}: not found.")


running = True

# game loop
while running:
    # run player moves
    for turn in range(Constants.NumPlayerMoves):
        command = input(">>> ")
        handleInput(command)

    # TODO: add event generator when done

