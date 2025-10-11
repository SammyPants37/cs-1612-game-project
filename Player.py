import Constants, random, Tile
from Constants import Minerals, ItemLimit, Items
class Player:

    def __init__(self):
        self.total_score: int = 0
        self.items: list[Items] = []
        self.minerals_in_bag: list[Minerals.mineralTypes] = []
        self.pos: tuple[int, int] = (-1, -1)
        self.actions_left: int = 0

    def add_score(self, new_mineral: Minerals.mineralTypes):
        self.minerals_in_bag.append(new_mineral) #adds mineral to bag
        self.total_score += new_mineral.score_value #adds mineral's score to total

    def grab_item(self, new_item: Items):
        if len(self.items) < Constants.ItemLimit: #if the amount of items in the list is less than 3
            self.items.append(new_item) #just add it to the list
            # TODO: add function that changes tile to no items
        else:
            for i in range(len(self.items)):
                if self.items[i] != new_item: #if there is a different item
                    self.items[i] = new_item #replace it with your new item
                    # TODO: add function that changes tile item value to opposite item
                    break #then stop looking
                #if all the items are the same as you are picking up nothing happens

    def setPos(self, pos: tuple[int, int]):
        self.pos = pos

    def inspect_tile(self):
        truth_2lies = Tile.mineral_forPos() #gives real and 2 fake minerals for the tile the player is on
        true_mineral = truth_2lies[0] #real mineral
        fake_mineral = truth_2lies[1] #is a list of 2 fakes
        true_mineral_pos = random.randint(1,3) #randomly generates a position for the real mineral every inspect, keeps order
        if true_mineral_pos == 1:
            said_mineral = [true_mineral, fake_mineral[0], fake_mineral[1]]
        elif true_mineral_pos == 2:
            said_mineral = [fake_mineral[1], true_mineral, fake_mineral[0]]
        else: #when true_mineral_pos is the 3rd position
            said_mineral = [fake_mineral[0], fake_mineral[1], true_mineral]
        print(f"Hmm... I think I could find {said_mineral[0]}, {said_mineral[1]}, or {said_mineral[2]} in this segment of the mine")
        # TODO:
        #  if the tile the player is on has an item:
        #    print(f"While gleaming the mine for potential minerals, I found {item on tile} that I could grab if space allows")

Player = Player() #to fulfill argument self with stuff