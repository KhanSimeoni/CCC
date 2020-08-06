import random
import time
import model
import value_functions as vf
import stop_conditions as sc

#path generator
def make_path(f, path=model.Path()):
    done = False
    while not done:
        building_vals = f(path)
        done = path.buy(vf.choose_best(building_vals))
    return path

#learning algorithm
def search(stop, funcs):
    #Finds the optimum weight value for choose_building to design a function
    time_passed = 0 # minutes since start of code
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
    path = make_path(lambda p: vf.weigh_functions(funcs, weights))
    counter = 0 #attempts since last improvement
    print(model.time_format(path.final_time))
    while not stop(path):
        #prints number of minutes passed
        time_passed = model.print_minutes(time_passed, 0)

        direction = vf.normalize([random.gauss(0, 1) for i in range(num)])
        new_weights = [weights[i] + (step_size * direction[i]) for i in range(num)]
        new = make_path(lambda p: vf.weigh_functions(funcs, weights))
        if new > path:
            print(model.time_format(new.final_time))
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

test, weights = search(sc.stop_time(1), [vf.rate_value, vf.excess_value, vf.time_value, vf.cps_value])
#print(test)
print(weights)
print(model.time_format(test.final_time))
#print(model.time_format(make_path(vf.rate_value).final_time))
