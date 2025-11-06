from typing import override
from Constants import Minerals
import Constants, random


def mineralRandomizer(wanted_list_size: int) -> list[Minerals.mineralTypes]:  # created a separate function so not to make the other line too long
    mineral = random.choices(list(Minerals.mineralTypes), weights=Minerals.weights, k=2)[0:wanted_list_size]
    return mineral #added k=2 above since needed 2 minerals for the fake ones


class Tile():

    def __init__(self, pos, resourceType: Minerals.mineralTypes, isExit: bool, fakeTypes: list[Minerals.mineralTypes]) -> None:
        self.pos: tuple[int, int] = pos
        self.resourceType: Minerals.mineralTypes = resourceType
        self.fakeTypes: list[Minerals.mineralTypes] = fakeTypes
        self.cavedIn: bool = False
        self.isDiscovered: bool = Constants.devMode # all tiles are pre-discovered in devMode
        self.isExit: bool = isExit
        self.hasMaulwurf: bool = False
        self.item: Constants.Items = Constants.Items.nothing
    
    def setItem(self, item: Constants.Items):
        self.item = item
    
    def setCavedIn(self, isCavedIn: bool):
        self.cavedIn = isCavedIn
        if isCavedIn: # if the tile is caved in
            self.hasMaulwurf = not isCavedIn # Maulwurf are now killed

    def drainMineral(self):
        self.resourceType = Minerals.mineralTypes.unminable

    def setMaulwurfStatus(self, hasMaulwurf: bool):
        self.hasMaulwurf = hasMaulwurf

    def is_usable(self, item: Constants.Items) -> bool: # checks for Maulwurf or CaveIn depending on item inputted
        if item == Constants.Items.dynamite:
            return self.cavedIn # returns whether it is cavedIn or not
        elif item == Constants.Items.weapon:
            return self.hasMaulwurf # returns whether it has a Maulwurf
        return False

    @override
    def __str__(self) -> str:
        if self.isExit:
            return "\033[36mE\033[0m" # returns E in cyan
        else:
            if self.isDiscovered:
                if self.cavedIn:
                    return "\033[31m#\033[0m" # returns # in red
                elif self.hasMaulwurf:
                    if self.resourceType == Minerals.mineralTypes.monsterDen:
                        return "\033[35mD\033[1:33m\u0336\033[0m" # returns D in purple with a bold yellow dash
                    return "\033[33mM\033[0m" # returns M in yellow
                elif self.item != Constants.Items.nothing:
                    bgrd = "\033[100m"
                else:
                    bgrd = ""
                match self.resourceType:
                    case Minerals.mineralTypes.unminable:
                        return f"{bgrd}\033[37m_\033[0m" # returns _ in gray
                    case Minerals.mineralTypes.monsterDen:
                        return f"{bgrd}\033[35mD\033[0m" # returns D in purple
                    case _:
                        return f"{bgrd}\033[32mO\033[0m" # returns O in green
            else:
                return "?"
