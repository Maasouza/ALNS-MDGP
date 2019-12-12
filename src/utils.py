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
