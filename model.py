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
        self.buildings = [[None, 0]]
        self.bought_extra = [None]
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

    #building_info takes the form (building, buy_extra)
    def buy(self, building_info):
        building = building_info[0]
        buy_extra = building_info[1]
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
            self.bought_extra.append(buy_extra)
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

    def replace(self, building_info, index):
        #changes should take the form: [(index, building), (index, building)]
        if index == 0: raise ValueError("Attempted to change 0th building")

        new = Path()
        for i in range(1, self.index + 1):
            if i == index: new.buy(building_info)
            else: new.buy((self.buildings[i][0], self.bought_extra[i]))

        return new

    def insert(self, building_info, index):
        if index == 0: raise ValueError("Attempted to change 0th building")

        new = Path()
        for i in range(1, self.index + 2):
            if i < index:
                building_info = (self.buildings[i][0], self.bought_extra[i])
                new.buy(building_info)
            elif i == index: new.buy(building_info)
            else:
                building_info = (self.buildings[i - 1][0], self.bought_extra[i - 1])
                new.buy(building_info)

        return new

    def remove(self, index):
        if index == 0: raise ValueError("Attempted to change 0th building")

        new = Path()
        for i in range(1, self.index + 1):
            if i != index:
                building_info = (self.buildings[i][0], self.bought_extra[i])
                new.buy(building_info)

        return new

#human readability
def print_minutes(min_passed, start_time):
    if int(time.time() - start_time) >= (min_passed + 1) * 60:
        min_passed += 1
        print(time_format(min_passed * 60))
    return min_passed

def minutes(n):
    return n * 60
