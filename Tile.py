from typing import override
from Constants import Minerals
import Constants, random, Player, main


def mineralRandomizer(wanted_list_size):  # created a separate function so not to make the other line too long
    mineral = random.choices(list(Minerals.mineralTypes), weights=Minerals.weights, k=2)[0:wanted_list_size]
    return mineral #added k=2 above since needed 2 minerals for the fake ones

def mineral_forPos(): #iterates over each tile of the map
    for row in main.map:
        coord = tuple(row[0]) #looks at tile position
        if coord == Player.Player.returnPos(): #compares to player pos
            return row[1:4:2] #returns real and fake, skipping isExit
    return None


class Tile():

    def __init__(self, pos, resourceType: Minerals.mineralTypes, isExit: bool, fakeTypes: list) -> None:
        self.pos: tuple[int, int] = pos
        self.resourceType: Minerals.mineralTypes = resourceType
        self.fakeTypes: list = fakeTypes
        self.cavedIn: bool = False
        self.isDiscovered: bool = False
        self.isExit: bool = isExit
        self.hasMaulwurf: bool = False
        self.item: Constants.Items = Constants.Items.nothing
    
    def setItem(self, item: Constants.Items):
        self.item = item
    
    def setCavedIn(self, isCavedIn: bool):
        self.cavedIn = isCavedIn

    def drainMineral(self):
        self.resourceType = Minerals.mineralTypes.unminable

    def setMaulwurfStatus(self, hasMaulwurf: bool):
        self.hasMaulwurf = hasMaulwurf

    @override
    def __str__(self) -> str:
        if self.isExit:
            return "E"
        else:
            if self.isDiscovered:
                if self.cavedIn:
                    return "#"
                elif self.hasMaulwurf:
                    return "M"
                match self.resourceType:
                    case Minerals.mineralTypes.unminable:
                        return "_"
                    case Minerals.mineralTypes.monsterDen:
                        return "D"
                    case _:
                        return "O"
            else:
                return "?"
