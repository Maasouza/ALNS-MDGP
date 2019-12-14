from simulation import *
from instance import *
from operators import Operator, InsertionOperator, RemovalOperator
from solution import *
from utils import *
from functions4operation import *
import time
import os

if __name__ == "__main__":
    num_repeats = 10
    path = '../data/mdgplib/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if any(i in file for i in ['10_ds_01', '10_ss_01', '12_ds_01', '12_ss_01', '30_ds_01', '30_ss_01', '60_ds_01', '60_ss_01', '120_ds_01', '120_ss_01', '240_ds_01', '240_ss_01', '480_ds_01', '480_ss_01', '960_ds_01', '960_ss_01' ]):
                files.append(os.path.join(r, file))

    files.sort()

    # print("instance_name, random, greedy_1, greedy_2, greedy_3_true, greedy_3_false")
    for file in files:
        instance = Instance(file)
        instance_name = file.split('/')[-1].split(".")[0]
        
        for i in range(num_repeats):
            print(instance_name, i)
            simulation = Simulation(instance)
            simulation.generate_random_solution()
            # print('# best until random:', simulation.best_solution)
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
            
            start_time = time.time()

            best_solutions, removal_operator, insertion_operator, itt_global= simulation.alns(
                max_itts=100, 
                initial_temperature=10**4, 
                final_temperature=10**(-3), 
                insertion_operators=insertion_operators, 
                removal_operators=removal_operators
            )
            end_time = time.time()

            write_to_file(instance_name, best_solutions, removal_operator, insertion_operator, end_time - start_time, itt_global, instance_name+"_"+str(i)+".out")

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
