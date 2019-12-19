from simulation import *
from instance import *
from operators import Operator, InsertionOperator, RemovalOperator
from solution import *
from utils import *
from functions4operation import *
import time
import os

if __name__ == "__main__":
    # Number of times the algorithm will execute for the problem.
    # In the end the best result of the repetitions can be analyzed.
    num_repeats = 5

    # True to use Simulated Annealing framework temperature reheat and False otherwise.
    reheat = False

    # List of instance files (with path) to be executed. 
    # This list can be constructed automatically (as comments below) or manually as:
    files = ['../data/surpresa/Surpresa_2_120_ds_16dez.txt']
    
    # files = []
    # path = '../data/mdgplib/RanReal/'
    # for r, d, f in os.walk(path):
    #     for file in f:
    #         if any(i in file for i in ['120_ds_01', '120_ss_01', '240_ds_01', '240_ss_01', '480_ds_01', '480_ss_01', '960_ds_01', '960_ss_01']):
    #             files.append(os.path.join(r, file))
    # files.sort()

    for file in files:
        instance = Instance(file)
        instance_name = file.split('/')[-1].split(".")[0]

        opts_info = []
        itts_global = []
        exec_times = []
        
        # Removal and insertion operators developed (with names)
        removal_functions = [[removal_1, 'Random'], [removal_2, "Biased Random"], [removal_3,"Greedy Least Contributor"], [removal_4,"Pair Shaw"], [removal_5,"Shaw"]]
        insertion_functions = [[insertion_1, 'Random'],[insertion_2, 'greedy mean diversity max'], [insertion_3, 'greedy mean diversity min'], [insertion_4, 'greedy mean diversity best group max'], [insertion_5, 'greedy mean diversity best group min'], [insertion_6, 'worst regret']]
        insertion_operators =  [InsertionOperator(*i) for i in insertion_functions]
        removal_operators = [RemovalOperator(*r) for r in removal_functions]

        for i in range(num_repeats):
            print(instance_name, i)

            simulation = Simulation(instance)

            # Initial solution used by the metaheuristics. 
            # If all options are uncommented the best found will be used.
            simulation.generate_random_solution()
            # simulation.greedy_solution_1()
            # simulation.greedy_solution_2()
            # simulation.greedy_solution_3(bestFirst=True)
            # simulation.greedy_solution_3(bestFirst=False)
            
            start_time = time.time()

            # ALNS Execution
            # The main parameters can be changed in this function call.
            best_solutions, removal_operator, insertion_operator, itt_global= simulation.alns(
                max_itts=50,                                # Maximum number of iterations of a segment.
                initial_temperature= 10**3,                 # Simulated Annealing framework initial temperature.
                final_temperature= 10**(-2),                # Simulated Annealing framework final temperature.
                insertion_operators=insertion_operators,    # All insertion operators that will be used by ALNS.
                removal_operators=removal_operators,        # All removal operators that will be used by ALNS.
                removal_rate = [0.2, 0.4],                  # Removal rate interval for solution deconstruction.
                reheat = reheat                             # True to use Simulated Annealing framework temperature reheat and False otherwise.
            )

            end_time = time.time()
            elapsed_time = end_time -start_time
            print('Execution time:', round(elapsed_time,3), 's')
            print('Best found:', best_solutions[-1][0],'\n')
            opts_info.append(best_solutions[-1])
            itts_global.append(itt_global)
            exec_times.append(elapsed_time)

            # Save results of one algorithm execution.
            write_to_file(instance_name, reheat, best_solutions, removal_operator, insertion_operator, elapsed_time, itt_global, instance_name+"_"+str(i)+".out")

            # Path-relinking execution.
            best_solution_path, enhanced = path_relinking(simulation.path_relink_solutions, instance)
            if enhanced:
                alns_type = "reheat_" if reheat else ""
                with open("../output/"+alns_type+"pathrelink_"+instance_name+"_"+str(i)+".out", 'w') as f:
                    f.write("Pathrelinking solution enhanced: "+str(best_solution_path.obj_value))

        # Save best results from all repetitions.
        write_all_itterations(instance_name, reheat, opts_info, itts_global, exec_times)
