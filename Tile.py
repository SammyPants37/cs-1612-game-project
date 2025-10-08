from typing import override
from Constants import Minerals
import Constants

class Tile():
    def __init__(self, pos, resourceType: Minerals.mineralTypes, isExit: bool) -> None:
        self.pos: tuple[int, int] = pos
        self.resourceType: Minerals.mineralTypes = resourceType
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

