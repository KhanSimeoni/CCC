#Framework
import sys
import random
sys.setrecursionlimit(100000000)

small_goal = 10000
goal = 1000000000
random_length = 9
num_bested = 0

def time_format(seconds):
    hours = 0
    minutes = 0
    while seconds > 3600:
        seconds -= 3600
        hours += 1
    while seconds > 60:
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

class Tree:
    def __init__(self, rate=10, total_cookies=0, time_elapsed=0, num_bought=[0]*9, building=None, parent=None):
        self.rate = rate
        self.total_cookies = total_cookies
        self.time_elapsed = time_elapsed
        self.num_bought = num_bought
        self.building = building
        self.nodes = []
        self.parent = parent

    def buy(self, building):
        cost = building.cost * (1.15 ** self.num_bought[building.num])
        time_needed = cost / self.rate
        if (time_needed < 0.01): time_needed = 0.01

        new_rate = self.rate + building.rate
        new_total_cookies = self.total_cookies + (self.rate * time_needed)
        new_time_elapsed = self.time_elapsed + time_needed
        new_num_bought = self.num_bought[:]
        new_num_bought[building.num] += 1
        new_building = building.name

        self.nodes.append(Tree(new_rate, new_total_cookies, new_time_elapsed, new_num_bought, new_building, self))

    def print_order(self):
        if(self.parent is not None):
            self.parent.print_order()
            print(self.building)


#Testing
def cost(current_tree, building):
    return building.cost * (1.15 ** current_tree.num_bought[building.num])

def cost_per_rate(current_tree, building):
    #lower value is better
    #returns very high values if takes too short to buy
    cost = cost(current_tree, building)
    rate = building.rate
    time_needed = cost / current_tree.rate
    if (time_needed < 0.01): return (8-building.num) * 16384
    else: return cost / rate

def building_vals(current_tree):
    #returns a list of  ordered by cost per rate
    ordered = []
    for b in buildings:
        ordered.append([b, cost_per_rate(current_tree, b)])
    ordered.sort(key = lambda x: x[1])
    final = []
    for item in ordered:
        final.append(item[0])
    return final

def random_buildings(current_tree):
    random_selection = []
    for r in range(random_length):
        random_selection.append(random.choice(buildings))
    return random_selection

best = [None]

def do_test(f, current_tree, building):
    global num_bested
    current_tree.buy(building)
    nextNode = current_tree.nodes[len(current_tree.nodes) - 1]
    if (nextNode.total_cookies < goal):
        f(nextNode)
    else:
        if (best[0] is None):
            best[0] = nextNode
        elif (nextNode.time_elapsed < best[0].time_elapsed):
            best[0] = nextNode
            num_bested = num_bested + 1
        #print("Time Elapsed: " + time_format(best[0].time_elapsed))
        #best[0].print_order()
        #print()

#def do_small_test(f, current_tree, building):
#    current_tree.buy(building)
#    nextNode = current_tree.nodes[len(current_tree.nodes) - 1]
#    if (nextNode.total_cookies < small_goal):
#        f(nextNode)
#    else:
#        if (best[0] is None):
#            best[0] = nextNode
#        elif (nextNode.time_elapsed < best[0].time_elapsed):
#            best[0] = nextNode
#        print("Time Elapsed: " + time_format(best[0].time_elapsed))
#        #best[0].print_order()
#        print()


#Strategies

#Buys only cursors
def buy_cursors(current_tree=Tree()):
    do_test(buy_cursors, current_tree, cursor)

#Brute forces every possible combination
def depth_first(current_tree=Tree()):
    for i in range(9): do_test(depth_first, current_tree, buildings[i])

def top3(current_tree=Tree()):
    ordered = building_vals(current_tree)
    for i in range(3): do_test(top2, current_tree, ordered[i])

#selects what to buy based on the cheapest option
def cheapest(current_tree=Tree()):
    best = cursor
    price = cost(current_tree, best)
    for b in buildings[1:]:
        new_price = cost(current_tree, b)
        if new_price < price:
            best = b
            price = new_price

    do_test(cheapest, current_tree, best)

#def mini_brute(current_tree=Tree()):
#    for i in range(9): do_small_test(mini_brute, current_tree, buildings[i])

#Selects what to buy randomly
test_limit = 5
tests_done = 0

random_selection = buildings
random.shuffle(random_selection)

def random_buy(current_tree=Tree()):
    global test_limit
    global tests_done

    tests_done = tests_done+1
    if test_limit > tests_done:
        for i in range(random_length-1):
                do_test(random_buy, current_tree, random_selection[i])
    else:
        print("bawdwddawdwadawdwadwadwddawdwadawdwadwade")




#buy_cursors()
#print_orderdepth_first()
#top3()
#cheapest()
#mini_brute()
random_buy()



#best[0].print_order()
print("Time Elapsed: " + time_format(best[0].time_elapsed))
print("________________________")
