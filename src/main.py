from simulation import *
from instance import *
from solution import *
import os

if __name__ == "__main__":
    path = '../data/mdgplib/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if any(i in file for i in ['10','12','30','60','120', '240', '480', '960']):
                files.append(os.path.join(r, file))

    # files.sort()
    files = [files[0]]
    
    print("instance_name, random, greedy_1, greedy_2, greedy_3_true, greedy_3_false")
    for file in files:
        instance = Instance(file)
        out = [file.split('/')[-1]]

        simulation = Simulation(instance)
        simulation.generate_random_solution()

        insertion_operators = []
        removal_operators = []

        simulation.alns(
            max_itts=50, 
            initial_temperature=10**4, 
            final_temperature=10**(-5), 
            insertion_operators=insertion_operators, 
            removal_operators=removal_operators
        )

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
