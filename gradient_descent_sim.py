import random
import time
import model
import value_functions as vf
import stop_conditions as sc

#path generator
def make_path(f, path):
    done = False
    while not done:
        building_vals = f(path)
        done = path.buy(vf.choose_best(building_vals))
    return path

#learning algorithm
def search(stop, funcs):
    #Finds the optimum weight value for choose_building to design a function
    time_passed = 0 # minutes since start of code
    start = time.time() #start time

    num = len(funcs)
    weights = []
    step_init = 1 # initial step size
    step_change = 1.5
    restart_point = 10*len(funcs) # how long to go without improvements before resetting step size

    #starts with a random weights
    for i in range(num):
        weights.append(random.uniform(-1, 1))

    #tests and adjusts weights
    step_size = ((step_init ** 2) * num) ** 0.5 #adjusts for number of weights
    path = make_path(vf.format_weights(funcs, weights), model.Path())
    counter = 0 #attempts since last improvement
    while not stop(path):
        #prints number of minutes passed
        time_passed = model.print_minutes(time_passed, start)

        direction = vf.normalize([random.gauss(0, 1) for i in range(num)])
        new_weights = vf.squish_weights([weights[i] + (step_size * direction[i]) for i in range(num)])

        new = make_path(vf.format_weights(funcs, weights), model.Path())
        if new != path:
            print("SOMETHING CHANGED")
        if new > path:
            path = new
            weights = new_weights
            step_size /= step_change
            counter = 0
        else:
            counter += 1
            if counter == restart_point:
                counter = 0
                step_size = ((random.random() ** 2) * num) ** 0.5

    return path, weights

test, weights = search(sc.stop_time(1, time.time()), [vf.rate_value, vf.excess_value, vf.time_value, vf.cps_value])
#print(test)
#print(weights)
print(model.time_format(test.final_time))
#print(model.time_format(make_path(vf.rate_value).final_time))
