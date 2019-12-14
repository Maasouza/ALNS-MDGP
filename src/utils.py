from math import exp, inf
import numpy as np
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

def path_relinking(solutions, instance):
    best_solution = max(solutions)

    path_worst_solution, path_best_solution = sorted(list(np.random.choice(solutions, 2, replace=False)))
    
    list_path_worst_solution, worst_group_bounds, worst_group_num_items, worst_viable = solution_to_list(path_worst_solution, instance.number_items)
    list_path_best_solution, best_group_bounds, best_group_num_items, best_viable = solution_to_list(path_best_solution, instance.number_items)

    # TODO fix


def solution_to_list(solution, number_items):
    solution_list = [-1] * number_items
    group_bounds = []
    group_num_items = []
    for id_group, group in enumerate(solution.groups):
        group_bounds.append((group.min_items, group.max_items))
        group_num_items.append(group.num_items)
        for item in group:
            solution_list[item] = id_group
    return solution_list, group_bounds, group_num_items, [True]*len(group_bounds)


def list_to_solution(solution_list, group_bounds, diversity_matrix):
    groups = []
    for min_bound, max_bound in group_bounds:
        groups.append(Group(min_bound, max_bound))
    
    for item, id_group in enumerate(solution_list):
        groups[id_group].add_item(item, diversity_matrix[item])
    
    return Solution(len(groups), group_bounds, groups)


def write_to_file(instance_name, reheat, best_solutions, removal_operator, insertion_operator, runtime, itt_global, file):
    alns_type = "reheat" if reheat else "normal"
    with open("../output/"+alns_type+"_"+file,'w') as f:
        f.write("Instancia: " + instance_name)
        f.write("\nExecution time: " + str(runtime))
        f.write("\nBest solution: " + str(best_solutions[-1][0]) + " at itteration " + str(best_solutions[-1][1]) + "/" + str(itt_global))
        f.write("\nRemoval Operators Weight")
        for name, weight in removal_operator:
            f.write("\n\t" + name + " - " + str(weight))
        f.write("\nInsertion Operators Weight")
        for name, weight in insertion_operator:
            f.write("\n\t" + name + " - " + str(weight))

    with open("../output/best_solutions_"+alns_type+"_"+file,'w') as f:
        for obj_val, itt in best_solutions:
            f.write("\n"+str(itt)+" "+str(obj_val))

def write_all_itterations(instance_name, opts_info, itts_global, exec_times):
    itt_average_time = []
    for idx in range(len(exec_times)):
        itt_average_time.append(exec_times[idx]/itts_global[idx])

    opt_max = 0
    opt_max_itt = inf

    opt_min = inf

    opts_values = []
    
    sum_itt_found_best = 0
    sum_avg_time_found_best = 0

    for idx in range(len(exec_times)):
        opts_values.append(opts_info[idx][0])

        if opts_info[idx][0] > opt_max:
            opt_max = opts_info[idx][0]
            opt_max_itt = opts_info[idx][1]
        elif opts_info[idx][0] == opt_max and opts_info[idx][1] < opt_max_itt:
            opt_max_itt = opts_info[idx][1]
        
        sum_itt_found_best += opts_info[idx][1]
        sum_avg_time_found_best += opts_info[idx][1] * itt_average_time[idx]

        if opts_info[idx][0] < opt_min:
            opt_min = opts_info[idx][0]

    with open('../output/info_' + instance_name + '.info', 'w') as f:
        f.write('Instancia: ' + instance_name)
        f.write('\n\tAvg exec time: ' + str(np.mean(exec_times)))
        f.write('\n\tAvg time to find best: ' + str(sum_avg_time_found_best/len(exec_times)))

        f.write('\n\tAvg exec itts: ' + str(np.mean(itts_global)))
        f.write('\n\tAvg itts to find best: ' + str(sum_itt_found_best/len(exec_times)))
        
        f.write('\nBest Solutions:')
        f.write('\n\tMax: ' + str(opt_max) + ' on itt: ' + str(opt_max_itt))
        f.write('\n\tMin: ' + str(opt_min))        
        f.write('\n\tAvg: ' + str(np.mean(opts_values)))
        f.write('\n\tStdDev: ' + str(np.std(opts_values)))
