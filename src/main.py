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
            if any(i in file for i in [ '10_ds_01', '120_ds_01', '120_ss_01', '240_ds_01', '240_ss_01', '480_ds_01', '480_ss_01', '960_ds_01', '960_ss_01' ]):
                files.append(os.path.join(r, file))

    files.sort()
    files = [files[0]]

    for file in files:
        instance = Instance(file)
        instance_name = file.split('/')[-1].split(".")[0]

        opts_info = []
        itts_global = []
        exec_times = []
        
        for i in range(num_repeats):
            print(instance_name, i)
            simulation = Simulation(instance)
            simulation.generate_random_solution()
            # simulation.greedy_solution_1()
            # simulation.greedy_solution_2()
            # simulation.greedy_solution_3(bestFirst=True)
            # simulation.greedy_solution_3(bestFirst=False)

            removal_functions = [[removal_1, 'Random'], [removal_2, "Biased Random"], [removal_3,"Greedy Least Contributor"], [removal_4,"Pair Shaw"], [removal_5,"Shaw"]]
            insertion_functions = [[insertion_1, 'Random'],[insertion_2, 'greedy mean diversity max'], [insertion_3, 'greedy mean diversity min'], [insertion_4, 'greedy mean diversity best group max'], [insertion_5, 'greedy mean diversity best group min'], [insertion_6, 'worst regret']]

            insertion_operators =  [InsertionOperator(*i) for i in insertion_functions]
            removal_operators = [RemovalOperator(*r) for r in removal_functions]
            
            start_time = time.time()
            reheat = False
            best_solutions, removal_operator, insertion_operator, itt_global= simulation.alns(
                max_itts=100, 
                initial_temperature=10**4, 
                final_temperature=10**(-3), 
                insertion_operators=insertion_operators, 
                removal_operators=removal_operators,
                removal_rate = [0.2, 0.4],
                reheat = reheat
            )
            end_time = time.time()
            elapsed_time = end_time -start_time

            opts_info.append(best_solutions[-1])
            itts_global.append(itt_global)
            exec_times.append(elapsed_time)

            write_to_file(instance_name, reheat, best_solutions, removal_operator, insertion_operator, elapsed_time, itt_global, instance_name+"_"+str(i)+".out")

            # path relink
            path_relinking(simulation.path_relink_solutions, instance)

        write_all_itterations(instance_name, opts_info, itts_global, exec_times)
        a = input()

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
