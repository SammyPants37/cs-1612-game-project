import Constants
from Constants import Minerals, ItemLimit, Items
from Constants import DenominatorEventsOccur as Events_scal
ansi: Constants.AnsiColors = Constants.AnsiColors()

def mineral_bag_amounts(self, weekday_num: int, day_of_month: int, week: int, month: int, year: int):
    print(f"------{ansi.bold_to_ital("Mineral Tally") + ansi.reset()}------")
    bonus_mult = (month / Events_scal) * (week + (19 * (year - 625177))) * (Events_scal ** (year - 625178))
    bonus_add = (weekday_num * day_of_month)
    total_bonus = 0
    for minerals in Constants.Minerals.mineralTypes:
        counter = 0
        bonus_score = 0
        for items in range(0, len(self.minerals_in_bag)):
            if minerals == self.minerals_in_bag[items]:
                counter += 1
            else: continue
            if minerals.code in (6,7,8,9,10,11,13):
                bonus_score += minerals.score_value
                total_bonus += minerals.score_value
        print(ansi.italics(f"{ansi.g_bold(minerals.description)} "
                           f"({ansi.g_bold(f"+{minerals.score_value:,}")}) {ansi.cyan(f"x {counter}")}" +
                           ansi.yellow(ansi.bold_to_ital(f" BONUS! (+{int(bonus_score * bonus_mult + (counter * bonus_add)):,})"))))
    print("-------------------------")
    return int(total_bonus * bonus_mult + (bonus_add * len(self.minerals_in_bag)))

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

    def exit_message(self, z_calendar: list):
        # z_calendar = [day_of_week, week, month, day_of_month, month_name, year, weekday_num]
        print(ansi.cyan("\nCongratulations -- you successfully escaped the mountains with your life!"))
        bonus_total = mineral_bag_amounts(self, z_calendar[6], z_calendar[3], z_calendar[1], z_calendar[2], z_calendar[5])
        print(ansi.g_bold(f"Mineral Score: {self.total_score:,}") +
              ansi.yellow(ansi.bold_to_ital(f"\n+ BONUS SCORE: {bonus_total:,}")) +
              ansi.cyan(ansi.bold_to_ital(f"\nFinal Score: {(self.total_score + bonus_total):,}")))
        print("-------------------------")
        if self.total_score / 2 >= 250000:
            print(ansi.italics("The mine yields to your mastery. Dwarves sing your name, carving it into stone so it may never be forgotten!"))
        elif self.total_score / 2 >= 100000:
            print(ansi.italics("You have returned with riches and tales, enough to retire you in comfort."))
        elif self.total_score / 2 >= 50000:
            print(ansi.italics("You have crawled from the depths, bruised and breathless. The mine have claimed your strength and offered little in return."))
        else:
            print(ansi.italics("You have crawled out with bones intact, but the mine still stands, unbroken and mocking your retreat."))

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
