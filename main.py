import random
from Constants import Minerals
from Constants import event_number_scaler

# rest of code goes here

class Day: #used to count the number of days that have passed
    def __init__(self):
        self.counter = 0
    def count_increase(self):
        self.counter += 1
Day = Day()

class Events: #calculates if an event has will occur based on the number of days passed
    def __init__(self):
        self.occurred_daily = 0

    def occurrence_probability(self):
        number_of_events = event_number_scaler(Day.counter) #sets number of events equal to the number off our formula
        while number_of_events > 0: #goes while potential events haven't occurred
            event_occurred = random.randint(1,6) #constant?, we'd likely just change the formula
            if event_occurred == 1: # creates the 1/6 chance of occurring
                self.occurred_daily += 1
            number_of_events -= 1
            self.occurred_daily = 0 # could be outside the while
            # insert func here that picks the event that would occur (which leads to the specific event's output)

        # self.occurred_daily = 0 # might want to include outside the loop, depends on other event funcs
Events = Events()

# *At the end of the turn loop: Events.occurrence_probability(), Day.count_increase()