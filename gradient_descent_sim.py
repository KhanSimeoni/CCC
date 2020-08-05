import random
import time

#Framework
FINAL_GOAL = 1000000000 #cookies
HUMAN_CLICK_SPEED = 14.0 #clicks per second
NOTATED_TIME_INTERVAL = 60 #seconds
START_TIME = time.time()

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

cursor = Building(15, 0.1, 0, "cursor")
grandma = Building(100, 0.5, 1, "grandma")
farm = Building(500, 4, 2, "farm")
factory = Building(3000, 10, 3, "factory")
mine = Building(10000, 40, 4, "mine")
shipment = Building(40000, 100, 5, "shipment")
lab = Building(200000, 400, 6, "lab")
portal = Building(1666666, 6666, 7, "portal")
time_machine = Building(123456789, 98765, 8, "time_machine")
buildings = [cursor, grandma, farm, factory, mine, shipment, lab, portal, time_machine]

class Path:
    def __init__(self):
        self.buildings = [[None, 0]]
        self.rate = [HUMAN_CLICK_SPEED]
        self.excess = [0.0]
        self.total_cookies = [0.0]
        self.time_elapsed = [0.0]
        self.num_bought = [[0]*len(buildings)]
        self.index = 0
        self.final_time = 0
        self.final_cookies = 0

    def cost_of(self, building, index, buy_extra):
        time_needed = 0
        num = 0
        cost = 0
        if buy_extra:
            max_num = 10
        else: max_num = 1
        excess = self.excess[index]
        while time_needed < (1 / HUMAN_CLICK_SPEED) and (num < max_num):
            cost += building.cost * (1.15 ** (self.num_bought[index][building.num]))
            if excess > cost:
                excess -= cost
                cost = 0
            else:
                cost -= excess
                excess = 0
            time_needed += cost / self.rate[index]
            num += 1
        if time_needed < 1 / HUMAN_CLICK_SPEED:
            excess += self.rate[index] * ((1 / HUMAN_CLICK_SPEED) - time_needed)
            time_needed = 1 / HUMAN_CLICK_SPEED
        return cost, time_needed, num, excess

    def buy(self, building, buy_extra=False):
        cost, time_needed, num, excess = self.cost_of(building, self.index, buy_extra)
        new_num_bought = self.num_bought[self.index][:]
        new_num_bought[building.num] += num
        if cost + self.total_cookies[self.index] < FINAL_GOAL:
            self.buildings.append([building, num])
            self.rate.append(self.rate[self.index] + (building.rate * num))
            self.total_cookies.append(self.total_cookies[self.index] + cost)
            self.time_elapsed.append(self.time_elapsed[self.index] + time_needed)
            self.num_bought.append(new_num_bought)
            self.excess.append(excess)
            self.index += 1
            return False
        else:
            cookies_needed = (FINAL_GOAL - self.total_cookies[self.index])
            time_needed = cookies_needed / self.rate[self.index]
            self.final_time = self.time_elapsed[self.index] + time_needed
            self.final_cookies = self.total_cookies[self.index] + (time_needed * self.rate[self.index])
            return True

    def __str__(self):
        name_list = "Building List:\n"
        for item in self.buildings[1:]:
            name_list += item[0].name + "\n"
            for i in range(1, item[1]):
                name_list += "   " + item[0].name + "\n"
        return name_list

    def __gt__(self, other):
        if self.final_time == 0: return False
        if other.final_time == 0: return True
        return self.final_time < other.final_time

    def __lt__(self, other):
        if other.final_time == 0: return False
        if self.final_time == 0: return True
        return self.final_time > other.final_time

    def __eq__(self, other):
        return self.final_time == other.final_time

    def __le__(self, other):
        if self.final_time == 0: return True
        if other.final_time == 0: return False
        return self.final_time >= other.final_time

    def __ge__(self, other):
        if other.final_time == 0: return True
        if self.final_time == 0: return False
        return self.final_time <= other.final_time



#Strategy
#returns the index of the max value in a list, returns randomly between equal values
def max_index(lst):
    max = lst[0]
    indexes = [0]
    for i in range(1, len(lst)):
        if lst[i] > max:
            max = lst[i]
            indexes = [i]
        elif lst[i] == max:
            indexes.append(i)
    return random.choice(indexes)

#path generator
def make_path(f):
    path = Path()
    done = False
    while not done:
        building_vals = f(path)
        index = max_index(building_vals)
        buy_extra = False
        if index >= len(buildings):
            index -= len(buildings)
            buy_extra = True
        done = path.buy(buildings[index], buy_extra)
    return path

#turns a vector into a unit vector with the same direction
def normalize(vector):
    #NO DIVIDING BY 0!!!!!
    magnitude = sum(x**2 for x in vector) ** 0.5
    if magnitude == 0: return vector
    return [x/magnitude for x in vector]

#value functions
def rate_value(path=Path()):
    #Value of a building is the exponential growth rate the building would imply
    vals = [0]*len(buildings)*2
    for i in range(len(buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(buildings[i], path.index, True)
        if path.total_cookies[path.index] + cost_one < FINAL_GOAL:
            vals[i] = (((buildings[i].rate * num_one) / path.rate[path.index]) + 1) ** (1 / time_needed_one)
        if path.total_cookies[path.index] + cost_ten < FINAL_GOAL:
            vals[i + len(buildings)] = (((buildings[i].rate * num_ten) / path.rate[path.index]) + 1) ** (1 / time_needed_ten)

    return normalize(vals)

def excess_value(path=Path()):
    #How much excess is created if said building is chosen
    vals = [0]*len(buildings)*2
    for i in range(len(buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(buildings[i], path.index, True)
        vals[i] += excess_one
        vals[i + len(buildings)] += excess_ten
        if path.total_cookies[path.index] + cost_one > FINAL_GOAL:
            vals[i] += FINAL_GOAL - path.total_cookies[path.index]
        if path.total_cookies[path.index] + cost_ten > FINAL_GOAL:
            vals[i + len(buildings)] += FINAL_GOAL - path.total_cookies[path.index]

    return normalize(vals)

def cps_value(path=Path()):
    #How much cps you get from a building
    vals = [0]*len(buildings)*2
    for i in range (len(buildings)):
        #cost_one, time_needed_one, num_one, excess_one = path.cost_of(buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(buildings[i], path.index, True)
        vals[i] = buildings[i].rate
        vals[i + len(buildings)] = buildings[i].rate * num_ten

    return normalize(vals)

def time_value(path=Path()):
    #How long a building takes to purchase
    vals = [0] * len(buildings) * 2
    for i in range (len(buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(buildings[i], path.index, True)
        vals[i] = time_needed_one
        vals[i + len(buildings)] = time_needed_ten

    return normalize(vals)


def weigh_functions(path, val_funcs, weights):
    if len(val_funcs) != len(weights): raise ValueError("Number of Functions and Weights don't match")
    for w in weights:
        if abs(w) > 1: raise ValueError("Weight not between -1 and 1")

    totals = [0]*len(buildings)*2
    for i in range(len(val_funcs)):
        vals = val_funcs[i](path)
        for j in range(len(buildings)):
            totals[j] += vals[j] * weights[i]
    return totals

#stop conditions
def stop_time(t):
    return lambda: START_TIME + t < time.time()


#human readability
def print_minutes(time_passed):
    if int(time.time() - START_TIME) >= (time_passed + 1) * 60:
        time_passed += 1
        print(time_format(time_passed * 60))
    return time_passed

#learning algorithm
def search(stop, funcs):
    #Finds the optimum weight value for choose_building to design a function
    time_passed = 0 # minutes since start of code
    num = len(funcs)
    weights = []
    restart_point = 10*len(funcs) # how long to go without improvements before resetting step size

    #starts with a random weights
    for i in range(num):
        weights.append(random.uniform(-1, 1))

    #tests and adjusts weights
    path = make_path(lambda p: weigh_functions(p, funcs, weights))

    counter = 0 #attempts since last improvement
    print(time_format(path.final_time))

    while not stop():
        #prints number of minutes passed
        time_passed = print_minutes(time_passed)
        

    return path, weights

test, weights = search(stop_time(1), [rate_value])
print(test)
print(weights)
print(time_format(test.final_time))
#print(time_format(make_path(rate_value).final_time))
