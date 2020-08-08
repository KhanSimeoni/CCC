import random
import time
import model
import value_functions as vf
import stop_conditions as sc

#Evolution Algorithm
def random_path(f, path):
    done = False
    while not done: done = path.buy(vf.choose_weighted(f(path)))
    return path

def evolution(stop, path, randomizer=vf.rate_value, starter=vf.rate_value):
    time_passed = 0
    start = time.time()

    #Make n changes, then compare to original. Keep whichever is better. Repeat until stop point
    while not stop(path):
        #prints the number of minutes passed
        time_passed = model.print_minutes(time_passed, start)
        #print(path)
        index = random.randint(1, path.index)

        #pick randomly whether to insert or remove a building
        toInsert = bool(random.getrandbits(1)) #picks randomly between True and False
        if toInsert:
            vals = randomizer(path)
            building = vf.choose_weighted(vals)
            new = path.insert(building, index)
        else:
            new = random_path(randomizer, path.remove(index))

        #keep the better path
        if new > path:
            path = new

    return path

#stop = sc.stop_time(model.minutes(30), time.time())
#test = evolution(stop, model.Path())
#print(test)
#print(model.time_format(test.final_time))


#test = Path()
#strat = [Farm, Farm, Farm, Grandma, Cursor, Cursor, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Grandma, Cursor, Farm, Factory, Factory, Mine, Mine, Mine, Factory, Farm, Grandma, Cursor, Cursor, Mine, Factory, Farm, Grandma, Cursor, Mine, Shipment, Factory, Mine, Farm, Grandma, Shipment, Factory, Mine, Farm, Grandma, Shipment, Factory, Shipment, Mine, Farm, Lab, Shipment, Lab, Lab, Factory, Mine, Farm, Lab, Portal, Portal, Portal, Portal, Portal, Portal, Portal, Portal, Lab, Shipment, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Lab, Shipment, Mine, Factory, Farm, Portal, Time_Machine, Time_Machine, Time_Machine, Lab, Time_Machine, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Portal, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Lab, Shipment, Shipment, Shipment, Shipment]
#for node in strat:
#    test.buy(node)
#print(time_format(test.final_time))
