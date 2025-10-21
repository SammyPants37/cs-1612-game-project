import Constants
from Constants import Minerals, ItemLimit, Items


class Player:


    def __init__(self):
        self.total_score: int = 0
        self.items: list[Items] = []
        for i in range(Constants.ItemLimit): #for as many items are in the item limit (contemporarily 3)
            self.items.append(Constants.Items.nothing) #add a nothing
        self.minerals_in_bag: list[Minerals.mineralTypes] = []
        self.pos: tuple[int, int] = (-1, -1)
        self.actions_left: int = 0

    def add_score(self, new_mineral: Minerals.mineralTypes):
        self.minerals_in_bag.append(new_mineral) #adds mineral to bag
        self.total_score += new_mineral.score_value #adds mineral's score to total

    def setPos(self, pos: tuple[int, int]):
        self.pos = pos

    def grab_item(self, new_item: Constants.Items):
        if new_item.value != 0: #if you aren't trying to grab nothing
            for i in range(Constants.ItemLimit): #iterates over all items in inventory
                if self.items[i].value == 0: #if there is a nothing item (no item)
                    self.items[i] = new_item #the first nothing in the list is replaced by the new item
                    print(f"{new_item.name} grabbed")
                    return Constants.Items.nothing #returns nothing to be dropped on the tile
                elif i == (Constants.ItemLimit - 1): #elif there are no nothing items
                    for j in range(Constants.ItemLimit): #iterates over items in inventory again
                        if self.items[j] != new_item: #finds if there is an item different from the grabbed one
                            dropped_item = self.items[j] # dropped item is defined as this different item
                            self.items[j] = new_item #the first different item in the list is replaced by the new item
                            print(f"{new_item.name} grabbed, {dropped_item.name} dropped")
                            return dropped_item
                        elif j == (Constants.ItemLimit - 1): #elif a different item is not found
                            print(f"{new_item.name} switched with {new_item.name}")
                            return new_item #drops the item grabbed
        else:
            print(f"{new_item.name} grabbed") #nothing is grabbed
            return new_item
