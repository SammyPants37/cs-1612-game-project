import Constants
from Constants import Minerals, ItemLimit

class Player:

    def __init__(self):
        self.total_score = 0
        self.items = []
        self.minerals_in_bag = []

    def add_score(self, new_mineral):
        self.minerals_in_bag.append(new_mineral.description) #adds mineral to bag
        self.total_score += new_mineral.score_value #adds mineral's score to total

    def grab_item(self, new_item):
        if len(self.items) < Constants.ItemLimit: #if the amount of items in the list is less than 3
            self.items.append(list(new_item)) #just add it to the list
            # TODO: add function that changes tile to no items
        else:
            for i in range(len(self.items)):
                if self.items[i] != new_item: #if there is a different item
                    self.items[i] = new_item #replace it with your new item
                    # TODO: add function that changes tile item value to opposite item
                    break #then stop looking
                #if all the items are the same as you are picking up nothing happens



