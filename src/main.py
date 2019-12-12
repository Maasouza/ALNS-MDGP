from simulation import *
from instance import *
from operators import Operator, InsertionOperator, RemovalOperator
from solution import *
from utils import *
from functions4operation import *

import os

if __name__ == "__main__":
    path = '../data/mdgplib/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if any(i in file for i in ['120', '240', '480', '960']):
                files.append(os.path.join(r, file))

    files.sort()
    files = [files[0]]

    # print("instance_name, random, greedy_1, greedy_2, greedy_3_true, greedy_3_false")
    for file in files:
        instance = Instance(file)
        out = [file.split('/')[-1]]
        print(out)

        simulation = Simulation(instance)
        simulation.generate_random_solution()

        insertion_operators = [InsertionOperator(insertion_1)]
        removal_operators = [RemovalOperator(removal_1)]

        simulation.alns(
            max_itts=100, 
            initial_temperature=10**4, 
            final_temperature=10**(-5), 
            insertion_operators=insertion_operators, 
            removal_operators=removal_operators
        )

        print("### BEST", simulation.best_solution)

    # out.append(simulation.current_solution.obj_value)
    # simulation.greedy_solution_1()
    # out.append(simulation.current_solution.obj_value)
    # simulation.greedy_solution_2()
    # out.append(simulation.current_solution.obj_value)
    # simulation.greedy_solution_3(True)
    # out.append(simulation.current_solution.obj_value)
    # simulation.greedy_solution_3(False)
    # out.append(simulation.current_solution.obj_value)
    # print(out)
