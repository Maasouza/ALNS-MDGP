from simulation import *
from instance import *
from solution import *
import os

if __name__ == "__main__":
    # instance = Instance('../data/mdgplib/RanReal/RanReal_n240_ss_09.txt')
    # alns = ALNS(instance)
    # alns.generate_random_solution()
    # print(alns.current_solution)
    # alns.greedy_solution_1()
    # print(alns.current_solution)
    # alns.greedy_solution_2()
    # print(alns.current_solution)
    # alns.greedy_solution_3(True)
    # print(alns.current_solution)
    path = '../data/mdgplib/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if any(i in file for i in ['10','12','30','60','120', '240', '480', '960']):
                files.append(os.path.join(r, file))

    files.sort()
    print("random, greedy_1, greedy_2, greedy_3_true, greedy_3_fals")
    for file in files:
        instance = Instance(file)
        out = [file.split('/')[-1]]

        alns = ALNS(instance)
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

