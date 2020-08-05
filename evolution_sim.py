import random
import time

#Framework
FINAL_GOAL = 1000000000 #cookies
HUMAN_CLICK_SPEED = 10.0 #clicks per second
NOTATED_TIME_INTERVAL = 60 #seconds

def time_format(seconds):
    seconds = int(seconds)
    hours = 0
    minutes = 0
    while seconds >= 3600:
        seconds -= 3600
        hours += 1
    while seconds >= 60:
        seconds -= 60
        minutes += 1
    return str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"

class Building:
    def __init__(self, cost, rate, num, name):
        self.cost = cost
        self.rate = rate
        self.num = num
        self.name = name

Cursor = Building(15, 0.1, 0, "cursor")
Grandma = Building(100, 0.5, 1, "grandma")
Farm = Building(500, 4, 2, "farm")
Factory = Building(3000, 10, 3, "factory")
Mine = Building(10000, 40, 4, "mine")
Shipment = Building(40000, 100, 5, "shipment")
Lab = Building(200000, 400, 6, "lab")
Portal = Building(1666666, 6666, 7, "portal")
Time_Machine = Building(123456789, 98765, 8, "time_machine")
buildings = [Cursor, Grandma, Farm, Factory, Mine, Shipment, Lab, Portal, Time_Machine]

class Path:
    def __init__(self):
        self.buildings = [None]
        self.rate = [HUMAN_CLICK_SPEED]
        self.total_cookies = [0.0]
        self.time_elapsed = [0.0]
        self.num_bought = [[0]*9]
        self.index = 0
        self.final_time = 0
        self.final_cookies = 0

    def costOf(self, building, index):
        cost = building.cost * (1.15 ** self.num_bought[self.index][building.num])
        time_needed = cost / self.rate[index]
        if time_needed < 0.01:
            time_needed = 0.1
            cost = self.rate[index] * time_needed
        return cost, time_needed

    def buy(self, building):
        new_num_bought = self.num_bought[self.index][:]
        new_num_bought[building.num] += 1
        cost, time_needed = self.costOf(building, self.index)
        if cost + self.total_cookies[self.index] < FINAL_GOAL:
            self.buildings.append(building)
            self.rate.append(self.rate[self.index] + building.rate)
            self.total_cookies.append(self.total_cookies[self.index] + cost)
            self.time_elapsed.append(self.time_elapsed[self.index] + time_needed)
            self.num_bought.append(new_num_bought)
            self.index += 1
            return False
        else:
            cookies_needed = (FINAL_GOAL - self.total_cookies[self.index])
            time_needed = cookies_needed / self.rate[self.index]
            self.final_time = self.time_elapsed[self.index] + time_needed
            self.final_cookies = self.total_cookies[self.index] + (time_needed * self.rate[self.index])
            return True

    def change(self, changes):
        #changes should take the form: [(index, building), (index, building)]
        changes.sort(key=lambda x: x[0])
        if changes[0][0] <= 0: raise ValueError("Attempted to change 0th building")

        new = Path()
        done = False
        for i in range(1, self.index + 1):
            if changes == [] or changes[0][0] != i:
                done = new.buy(self.buildings[i])
            else:
                done = new.buy(changes.pop(0)[1])
            if done: break
        return new

    def __str__(self):
        name_list = "Building List:\n"
        for item in self.buildings[1:]:
            name_list += "   " + item.name + "\n"
        return name_list


#Strategy
def compare(path1, path2):
    if path1.final_time < path2.final_time: return path1
    else: return path2

#Randomizer functions
#index refers to the last index before the change being made
def by_equal(path, index):
    return random.choice(buildings)

def by_value(path, index):
    weights = []
    for building in buildings:
        cost, time_needed = path.costOf(building, index - 1)
        weights.append(building.rate / cost)
    total = sum(weights)
    for i in range(9):
        weights[i] = (weights[i] / total) + 0.1
    return random.choices(buildings, weights)[0]

def by_exponential_growth_rate(path, index):
    #not random
    vals = []
    for building in buildings:
        cost, time_needed = path.costOf(building, index - 1)
        if path.total_cookies[index - 1] + cost >= FINAL_GOAL:
            vals.append(0)
        else:
            vals.append(((building.rate / path.rate[index - 1]) + 1) ** (1 / time_needed))
    return buildings[vals.index(max(vals))]

#Evolution Algorithm
def random_path(f, p=Path()):
    done = False
    while not done:
        done = p.buy(f(p, p.index + 1))
    return p

def evolution(t, n=1, randomizer=by_equal, starter=by_exponential_growth_rate, current=None):
    print("running for " + time_format(t))

    #Start with random path
    if current is None: current = random_path(starter)

    #Make n changes, then compare to original. Keep whichever is better. Repeat until stop point
    start_time = time.time()
    prev_time = start_time
    current_time = start_time
    while current_time < start_time + t:
        indexes = list(range(1, current.index + 1))
        changes = []
        for i in range(n):
            change = random.choice(indexes)
            indexes.remove(change)
            changes.append((change, randomizer(current, change)))
        new = random_path(randomizer, current.change(changes))
        current = compare(current, new)

        current_time = time.time()
        if current_time >= prev_time + NOTATED_TIME_INTERVAL:
            print(time_format(current_time - start_time))
            prev_time = current_time

    return current


test = random_path(by_exponential_growth_rate)
print(test)
print(time_format(test.final_time))

#test = Path()
#strat = [Farm, Farm, Farm, Grandma, Cursor, Cursor, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Factory, Factory, Mine, Mine, Mine, Factory, Farm, Grandma, Cursor, Cursor, Mine, Factory, Farm, Grandma, Cursor, Mine, Shipment, Factory, Mine, Farm, Grandma, Shipment, Factory, Mine, Farm, Grandma, Shipment, Factory, Shipment, Mine, Farm, Lab, Shipment, Lab, Lab, Factory, Mine, Farm, Lab, Portal, Portal, Portal, Portal, Portal, Portal, Portal, Portal, Lab, Shipment, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Time_Machine, Time_Machine, Time_Machine, Lab, Time_Machine, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Shipment, Shipment, Shipment]
#for node in strat:
#    test.buy(node)
#print(time_format(test.final_time))
