import random
import time

#Framework
FINAL_GOAL = 1000000000 #cookies
HUMAN_CLICK_SPEED = 10.0 #clicks per second
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

    def cost_of(self, building, index=self.index):
        time_needed = 0
        num = 0
        excess = self.excess[index]
        while time_needed < 1 / HUMAN_CLICK_SPEED and num < 10:
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
        return cost, time_needed, num, excess

    def buy(self, building):
        cost, time_needed, num, excess = self.cost_of(building, self.index)
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
            name_list += "   " + item.name + "\n"
        return name_list

    def __cmp__(self, other):
        if other.final_time == 0: return self.final_time
        elif self.final_time == 0: return -1
        return other.final_time - self.final_time



#Strategy
#path generator
def make_path(f):
    path = Path()
    done = False
    while not done:
        building_vals = f(path)
        done = path.buy(building_vals.index(max(building_vals)))
    return path

#squishes values to be between 0 and 1
def squisher(val_list):
    #NO DIVIDING BY 0!!!!!
    s = sum(val_list)
    if s == 0: return val_list

    for i in range(len(val_list)):
        val_list[i] /= s

    return val_list

#value functions
def rate_value(path=Path()):
    #Value of a building is the exponential growth rate the building would imply
    vals = [0]*len(buildings)
    for i in range(len(buildings)):
        cost, time_needed, num, excess = path.cost_of(buildings[i], path.index)
        if path.total_cookies[path.index] + cost < FINAL_GOAL:
            vals[i] = (((building.rate * num) / path.rate[index - 1]) + 1) ** (1 / time_needed)

    return squisher(vals)

def excess_value(path=Path()):
    #How much excess is created if said building is chosen
    vals = [0]*len(building)
    for i in range(len(buildings)):
        cost, time_needed, num, excess = path.cost_of(buildings[i], path.index)
        vals[i] += excess
        if path.total_cookies[path.index] + cost > FINAL_GOAL:
            vals[i] += FINAL_GOAL - path.total_cookies[path.index]

    return squisher(vals)






def weigh_functions(path, val_funcs, weights):
    if len(val_funcs) != len(weights): raise ValueError("Number of Functions and Weights don't match")
    for w in weights:
        if abs(w) > 1: raise ValueError("Weight not between -1 and 1")

    totals = [0]*len(buildings)
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
    if int(time.time() - START_TIME) > m_prev:
        time_passed += 1
        print(time_format(m_prev * 60))
    return time_passed

#genetic algorithm
def genetic(stop):
    #Finds the optimum weight value for choose_building to design a function

    #starts with a random weights
    funcs = [rate_value, excess_value]
    weights = []
    for i in range(len(funcs)):
        weights.append(random.uniform(-1, 1))

    #test and adjust weights
    current = make_path(lambda p: weigh_functions(p, funcs, weights))
    while not stop():
        #prints number of minutes passed
        time_passed = print_minutes(time_passed)



    return path

#test = genetic(stop_time(10))
#test = make_path(valueOf)
#print(p)
