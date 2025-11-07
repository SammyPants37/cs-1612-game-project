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

    def exit_message(self):
        print("Congratulations -- you successfully escaped the mountains with your life!")
        print(f"Score: {self.total_score}")
        if self.total_score >= 250000:
            print( "The mine yields to your mastery. Dwarves sing your name, carving it into stone so it may never be forgotten!")
        elif self.total_score >= 100000:
            print("You have returned with riches and tales, enough to retire you in comfort.")
        elif self.total_score >= 50000:
            print("You have crawled from the depths, bruised and breathless. The mine have claimed your strength and offered little in return.")
        else:
            print("You have crawled out with bones intact, but the mine still stands, unbroken and mocking your retreat.")

    # TODO: save and show game stats and prompt to "play again?"

    def setPos(self, pos: tuple[int, int]):
        self.pos = pos

    def grab_item(self, new_item: Constants.Items):
        if new_item.value != 0: #if you aren't trying to grab nothing
            for given_item in self.items: #iterates over all items in inventory
                if given_item.value == 0: #if the item you are on is nothing
                    self.items[self.items.index(given_item)] = new_item # 1st nothing in the list is replaced by the new item
                    print(f"{new_item.name} grabbed")
                    return Constants.Items.nothing #returns nothing to be dropped on the tile
            for given_item in self.items: #iterates over items in inventory again
                if given_item != new_item: #finds if there is an item different from the grabbed one
                    self.items[self.items.index(given_item)] = new_item # 1st different item in the list is replaced by the new item
                    print(f"{new_item.name} grabbed, {given_item.name} dropped")
                    return given_item #returns the different item to be dropped, not overwritten when list changed since local
        print(f"{new_item.name} grabbed, {new_item.name} dropped") #nothing is grabbed or dropped (or same thing is)
        return new_item
