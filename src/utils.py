from math import exp
from solution import *
import random

def boltzman(delta, temperature):
    return exp(delta/temperature)

def roulette(elements, weights):
    sum_weight = sum(weights)
    unif = random.random()
    cum_sum = 0
    for idx, weight in enumerate(weights):
        cum_sum += float(weight)/sum_weight
        if cum_sum > unif:
            return elements[idx]

def write_to_file(instance_name, best_solutions, removal_operator, insertion_operator, runtime, itt_global, file):
    with open("../output/"+file,'w') as f:
        f.write("Instancia: " + instance_name)
        f.write("\nExecution time: " + str(runtime))
        f.write("\nBest solution: " + str(best_solutions[-1][0]) + " at itteration " + str(best_solutions[-1][1]) + "/" + str(itt_global))
        f.write("\nRemoval Operators Weight")
        for name, weight in removal_operator:
            f.write("\n\t" + name + " - " + str(weight))
        f.write("\nInsertion Operators Weight")
        for name, weight in insertion_operator:
            f.write("\n\t" + name + " - " + str(weight))

    with open("../output/best_solutions_"+file,'w') as f:
        for obj_val, itt in best_solutions:
            f.write("\n"+str(itt)+" "+str(obj_val))