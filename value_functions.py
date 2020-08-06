import model
import random

#turns a vector into a unit vector with the same direction
def normalize(vector):
    #NO DIVIDING BY 0!!!!!
    magnitude = sum(x**2 for x in vector) ** 0.5
    if magnitude == 0: return vector
    return [x/magnitude for x in vector]

#Gives all buildings equal value
def equal_value(path=model.Path()):
    return normalize([1] * len(model.buildings) * 2)

#How much excess is created if said building is chosen
def excess_value(path=model.Path()):
    vals = [0]*len(model.buildings)*2
    for i in range(len(model.buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(model.buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(model.buildings[i], path.index, True)
        vals[i] += excess_one
        vals[i + len(model.buildings)] += excess_ten
        if path.total_cookies[path.index] + cost_one > model.FINAL_GOAL:
            vals[i] += model.FINAL_GOAL - path.total_cookies[path.index]
        if path.total_cookies[path.index] + cost_ten > model.FINAL_GOAL:
            vals[i + len(model.buildings)] += model.FINAL_GOAL - path.total_cookies[path.index]

    return normalize(vals)

#How much cps you get from a building
def cps_value(path=model.Path()):
    vals = [0]*len(model.buildings)*2
    for i in range (len(model.buildings)):
        #cost_one, time_needed_one, num_one, excess_one = path.cost_of(model.buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(model.buildings[i], path.index, True)
        vals[i] = model.buildings[i].rate
        vals[i + len(model.buildings)] = model.buildings[i].rate * num_ten

    return normalize(vals)

#Value of a building is the exponential growth rate the building would imply
def rate_value(path=model.Path()):
    vals = [0]*len(model.buildings)*2
    for i in range(len(model.buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(model.buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(model.buildings[i], path.index, True)
        if path.total_cookies[path.index] + cost_one < model.FINAL_GOAL:
            vals[i] = (((model.buildings[i].rate * num_one) / path.rate[path.index]) + 1) ** (1 / time_needed_one)
        if path.total_cookies[path.index] + cost_ten < model.FINAL_GOAL:
            vals[i + len(model.buildings)] = (((model.buildings[i].rate * num_ten) / path.rate[path.index]) + 1) ** (1 / time_needed_ten)

    return normalize(vals)

#How long a building takes to purchase
def time_value(path=model.Path()):
    vals = [0] * len(model.buildings) * 2
    for i in range (len(model.buildings)):
        cost_one, time_needed_one, num_one, excess_one = path.cost_of(model.buildings[i], path.index, False)
        cost_ten, time_needed_ten, num_ten, excess_ten = path.cost_of(model.buildings[i], path.index, True)
        vals[i] = time_needed_one
        vals[i + len(model.buildings)] = time_needed_ten

    return normalize(vals)

#combines the return values of multiple value functions into a single one
def weigh_functions(val_funcs, weights, path=model.Path()):
    if len(val_funcs) != len(weights): raise ValueError("Number of Functions and Weights don't match")
    for w in weights:
        if abs(w) > 1: raise ValueError("Weight not between -1 and 1")

    totals = [0]*len(model.buildings)*2
    for i in range(len(val_funcs)):
        vals = val_funcs[i](path)
        for j in range(len(model.buildings)):
            totals[j] += vals[j] * weights[i]
    return totals

#returns the building found at a specific index, accounting for buy_extra
def building_at(index):
    buy_extra = False
    if index >= len(model.buildings):
        buy_extra = True
        index -= len(model.buildings)
    return model.buildings[index], buy_extra

#returns the building with the highest value
def choose_best(vals):
    max = vals[0]
    indexes = [0]
    for i in range(1, len(vals)):
        if vals[i] > max:
            max = vals[i]
            indexes = [i]
        elif vals[i] == max:
            indexes.append(i)

    index = random.choice(indexes)
    return building_at(index)

#returns a random building weighted by value
def choose_weighted(vals):
    index = random.choices([i for i in range(len(vals))], vals)[0]
    return building_at(index)
