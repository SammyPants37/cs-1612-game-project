from typing import override
from Constants import Minerals
import Constants, random
ansi: Constants.AnsiColors = Constants.AnsiColors()

def mineralRandomizer(wanted_list_size: int) -> list[Minerals.mineralTypes]:  # created a separate function so not to make the other line too long
    mineral = random.choices(list(Minerals.mineralTypes), weights=Minerals.weights[wanted_list_size - 1], k=2)[0:wanted_list_size]
    return mineral #added k=2 above since needed 2 minerals for the fake ones


class Tile():
    """main class for a tile. one instance of this is created for every tile on the map"""
    def __init__(self, pos, resourceType: Minerals.mineralTypes, isExit: bool, fakeTypes: list[Minerals.mineralTypes]) -> None:
        self.pos: tuple[int, int] = pos
        self.resourceType: Minerals.mineralTypes = resourceType
        self.fakeTypes: list[Minerals.mineralTypes] = fakeTypes
        self.cavedIn: bool = False
        self.isDiscovered: bool = Constants.devMode # all tiles are pre-discovered in devMode
        self.isExit: bool = isExit
        self.hasMaulwurf: bool = False
        self.item: Constants.Items = Constants.Items.nothing

    def make_discovered(self):
        """discover a tile"""
        self.isDiscovered = True

    def setItem(self, item: Constants.Items):
        """set the item on a tile"""
        self.item = item

    def setCavedIn(self, isCavedIn: bool):
        """set the caved in status"""
        self.cavedIn = isCavedIn
        if isCavedIn: # if the tile is caved in
            self.hasMaulwurf = not isCavedIn # Maulwurf are now killed

    def drainMineral(self):
        """remove the mineral from the tile"""
        self.resourceType = Minerals.mineralTypes.unminable

    def setMaulwurfStatus(self, hasMaulwurf: bool):
        """set the maulwurf status of the tile"""
        self.hasMaulwurf = hasMaulwurf

    def is_usable(self, item: Constants.Items) -> bool: # checks for Maulwurf or CaveIn depending on item inputted
        """check if an item is usable on this tile"""
        if item == Constants.Items.dynamite:
            return self.cavedIn # returns whether it is cavedIn or not
        elif item == Constants.Items.weapon:
            return self.hasMaulwurf # returns whether it has a Maulwurf
        return False

    @override
    def __str__(self) -> str:
        """return a single character when str(tile) is called"""
        if self.isExit:
            return ansi.cyan("E") # returns E in cyan
        else:
            if self.isDiscovered:
                if self.cavedIn:
                    return ansi.red("#") # returns # in red
                elif self.hasMaulwurf:
                    if self.resourceType == Minerals.mineralTypes.monsterDen:
                        return ansi.purp_ydash("D") # returns D in purple with a bold yellow dash
                    return ansi.yellow("M") # returns M in yellow
                elif self.item != Constants.Items.nothing:
                    bgrd = ansi.graybgrd("")
                else:
                    bgrd = ""
                match self.resourceType:
                    case Minerals.mineralTypes.unminable:
                        return bgrd + ansi.gray("_") # returns _ in gray
                    case Minerals.mineralTypes.monsterDen:
                        return bgrd + ansi.purple("D") # returns D in purple
                    case _:
                        return bgrd + ansi.green("O") # returns O in green
            else:
                return "?"
