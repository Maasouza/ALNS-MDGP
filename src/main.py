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

    files.sort()
    print("instance_name, random, greedy_1, greedy_2, greedy_3_true, greedy_3_false")
    for file in files:
        instance = Instance(file)
        out = [file.split('/')[-1]]

        alns = Simulation(instance)
        alns.generate_random_solution()
        out.append(alns.current_solution.obj_value)
        alns.greedy_solution_1()
        out.append(alns.current_solution.obj_value)
        alns.greedy_solution_2()
        out.append(alns.current_solution.obj_value)
        alns.greedy_solution_3(True)
        out.append(alns.current_solution.obj_value)
        alns.greedy_solution_3(False)
        out.append(alns.current_solution.obj_value)
        print(out)
