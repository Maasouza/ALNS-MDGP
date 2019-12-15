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

def path_relinking(sols, instance):
    
    solutions = sols[:]
    best_obj_val = max(solutions).obj_value
    best_solution = None
    enhanced = False
    while len(solutions) > 1:

        target_sol, start_sol = sorted(list(np.random.choice(solutions, 2, replace=False)))
        
        worst_solution_items = solution_to_list(target_sol, instance.number_items)
        best_solution_items = solution_to_list(start_sol, instance.number_items)

        moves_to_be_made = []

        for item in range(instance.number_items):
            group_id_best = best_solution_items[item]
            group_id_worst = worst_solution_items[item]
            if group_id_worst != group_id_best:
                moves_to_be_made.append([item, group_id_best, group_id_worst])
        
        while len(moves_to_be_made) > 0:
            best_id = None
            best_gain_value = -inf
            for i in range(len(moves_to_be_made)):
                item, remove_from, add_to = moves_to_be_made[i]
                
                lost = 0
                if start_sol.groups[remove_from].num_items > 1:
                
                    lost = float(start_sol.groups[remove_from].items[item])/float(start_sol.groups[remove_from].num_items - 1) 

                gain = 0
                if start_sol.groups[add_to].num_items > 0:
                    gain = start_sol.groups[add_to].evaluate_item(item, instance.adj_matrix[item])

                if (gain-lost) > best_gain_value:
                    best_gain_value = gain - lost
                    best_id = i
              
            item, remove_from, add_to = moves_to_be_made[best_id]
            
            start_sol.groups[remove_from].remove_item(item, instance.adj_matrix[item])
            start_sol.groups[add_to].add_item(item, instance.adj_matrix[item])

            del moves_to_be_made[best_id]
                
            if start_sol.is_valid_solution():
                start_sol.update_obj_value()
                if start_sol.obj_value > best_obj_val:
                    best_obj_val = start_sol.obj_value 
                    best_solution = start_sol.copy()
                    enhanced = True

        solutions.remove(start_sol)
        solutions.remove(target_sol)
    return best_solution.copy(), enhanced
    


def solution_to_list(solution, number_items):
    solution_list = [None]*number_items
    solution.groups.sort(key = lambda x: x.id_group)
    for id_group, group in enumerate(solution.groups):
        for item in group.items:
            solution_list[item] = id_group
    return solution_list


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
