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
            if any(i in file for i in ['960']):
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
        print('# best until random:', simulation.best_solution)
        # simulation.greedy_solution_1()
        # print('# best until greedy_1:', simulation.best_solution)
        # simulation.greedy_solution_2()
        # print('# best until greedy_2:', simulation.best_solution)
        # simulation.greedy_solution_3(bestFirst=True)
        # print('# best until greedy_3-true:', simulation.best_solution)
        # simulation.greedy_solution_3(bestFirst=False)
        # print('# best until greedy_3-false:', simulation.best_solution)

        # simulation.current_solution = simulation.best_solution.copy()

        removal_functions = [[removal_1, 'Random'], [removal_2, "Biased Random"], [removal_3,"Greedy Least Contributor"], [removal_4,"Pair Shaw"], [removal_5,"Shaw"]]
        insertion_functions = [[insertion_1, 'Random'],[insertion_2, 'greedy mean diversity max'], [insertion_3, 'greedy mean diversity min'], [insertion_4, 'greedy mean diversity best group max'], [insertion_5, 'greedy mean diversity best group min'], [insertion_6, 'worst regret']]

        insertion_operators =  [InsertionOperator(*i) for i in insertion_functions]
        removal_operators = [RemovalOperator(*r) for r in removal_functions]

        simulation.alns(
            max_itts=100, 
            initial_temperature=10**5, 
            final_temperature=10**(-4), 
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
