from instance import *
from solution import *
from utils import *
from queue import PriorityQueue
import random
from functions4operation import repair

class Simulation:
    
    def __init__(self, instance):
        self.instance = instance
        self.items = set(range(instance.number_items))
        self.current_solution = None
        self.best_solution = None
        self.path_relink_solutions = []

    def generate_random_solution(self):
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(i, lower_bound, upper_bound))
        
        for item in self.items:
            included = False
            while not included:
                idx = random.choices(range(self.instance.number_groups))[0]
                included = groups[idx].add_item_if_viable(item, self.instance.adj_matrix[item])

        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        
        repair(self.current_solution, self.instance)

        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_1(self):
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(i, lower_bound, upper_bound))

        pairs = []
        for i in range(self.instance.number_items-1):
            for j in range(i+1, self.instance.number_items):
                pairs.append((i,j,self.instance.adj_matrix[i][j]))
       
        pairs.sort(key=lambda x: x[2], reverse=True)
        used_items = set()
        select_group = 0
        for i, j, _ in pairs:
            if i not in used_items:
                if groups[select_group].add_item_if_viable(i, self.instance.adj_matrix[i]):
                    used_items.add(i)
                else:
                    select_group+=1

            if j not in used_items:
                if groups[select_group].add_item_if_viable(j, self.instance.adj_matrix[j]):
                    used_items.add(j)
                else:
                    select_group+=1
        
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
       
        repair(self.current_solution, self.instance)

        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_2(self):

        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(i, lower_bound, upper_bound))

        mean_diversity = []
        for item, item_diversity in enumerate(self.instance.adj_matrix):
            mean_diversity.append( (item, sum(item_diversity) / float( len(item_diversity) - 1) ) )

        mean_diversity.sort(key=lambda x:x[1], reverse = True) 
       
        select_group = 0
        for i, _ in mean_diversity:
            while not groups[select_group].add_item_if_viable(i, self.instance.adj_matrix[i]):
               select_group+=1
            
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
      
        repair(self.current_solution, self.instance)
      
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_3(self, bestFirst):
        
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(i, lower_bound, upper_bound))

        mean_diversity = []
        for item, item_diversity in enumerate(self.instance.adj_matrix):
            mean_diversity.append( (item, sum(item_diversity) / float( len(item_diversity) - 1) ) )

        mean_diversity.sort(key=lambda x:x[1], reverse = bestFirst)

        for i in range(self.instance.number_groups):
            # adiciona os utimos em cada grupo
            item, _ = mean_diversity.pop()
            groups[i].add_item_if_viable(item, self.instance.adj_matrix[item])
        
        for item, _ in mean_diversity:
            evaluated_gains = PriorityQueue()
            added = False
            for i, group in enumerate(groups):
                evaluated_gains.put( ( ((-1) * group.evaluate_item(item, self.instance.adj_matrix[item]), i ) ))
            
            while not added:
                _, group_index = evaluated_gains.get()
                added = groups[group_index].add_item_if_viable(item, self.instance.adj_matrix[item])
        
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        
        repair(self.current_solution, self.instance)
        
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def __update_weights(self, operators, weights, r=0.2):
        for idx, operator in enumerate(operators):
            if operator.score != 0 and operator.times_used != 0:
                # weights[idx] = weights[idx] * (1-r) + r * (operator.score/operator.times_used)
                weights[idx] = weights[idx] + r * (operator.score/operator.times_used)
            operator.reset_score()
            operator.reset_times_used()


    def alns(self, max_itts, initial_temperature, final_temperature, insertion_operators, removal_operators, removal_rate=[0.3, 0.5], reheat=False):
        current_temperature = initial_temperature

        removal_weights = [ 1.0 ] * len(removal_operators) 
        insertion_weights = [ 1.0 ] * len(insertion_operators) 
        
        current_removal_rate = removal_rate[0]

        itt_global = 0
        itt_without_enhancement = 0
        max_itt_without_enhancement = 2*max_itts
        
        reheat_times = 0

        best_solutions = [] #[(obj_best_itt, itt)]

        while current_temperature >= final_temperature:
            itt_segment = 0
            

            while itt_segment < max_itts:
                
                new_solution = self.current_solution.copy()
                
                removal_operator = roulette(removal_operators, removal_weights)
                removed_items = removal_operator.execute(new_solution, self.instance, current_removal_rate)
                new_solution.update_obj_value()

                insertion_operator = roulette(insertion_operators, insertion_weights)
                insertion_operator.execute(new_solution, self.instance, removed_items)
                new_solution.update_obj_value()
                
                solution_change = False
                if new_solution > self.current_solution:
                    self.current_solution = new_solution.copy()
                    solution_change = True
                    if self.current_solution > self.best_solution:
                        best_temperature = current_temperature
                        current_removal_rate = removal_rate[0]
                        reheat_times = 0
                        self.best_solution = self.current_solution.copy()
                        # print("### Best", self.best_solution)
                        best_solutions.append((self.best_solution.obj_value, itt_global))
                        self.path_relink_solutions.append(self.best_solution.copy())
                        # sigma_1 points
                        sigma_1 = 5.0
                        removal_operator.increment(sigma_1)
                        insertion_operator.increment(sigma_1)
                    
                    else:
                        # sigma_2 points
                        sigma_2 = 1.0
                        removal_operator.increment(sigma_2)
                        insertion_operator.increment(sigma_2)

                else:
                    if new_solution != self.current_solution:
                        delta_solution = new_solution.obj_value - self.current_solution.obj_value
                        # accepted by simulated annealing criteria
                        if random.random() < boltzman(delta_solution, current_temperature):
                            self.current_solution = new_solution.copy()
                            # sigma_3 points
                            sigma_3 = 3.0
                            removal_operator.increment(sigma_3)
                            insertion_operator.increment(sigma_3)   

                if solution_change:
                    itt_without_enhancement = 0
                    # current_removal_rate = removal_rate[0]
                else:
                    itt_without_enhancement +=1 
                    current_removal_rate = min( removal_rate[1], removal_rate[0] + (removal_rate[1] - removal_rate[0])*(itt_without_enhancement/max_itt_without_enhancement))

                if reheat and itt_without_enhancement > max_itt_without_enhancement :
                    itt_without_enhancement = 0
                    reheat_times += 1
                    current_temperature  = max(best_temperature/reheat_times, current_temperature)
                    if random.random() > 0.1:
                        self.generate_random_solution()
                    else:
                        self.current_solution = self.best_solution.copy()
                        
                itt_segment += 1
                itt_global += 1
            
            current_temperature *= 0.9 # cooling
            
            # for op in removal_operators:
            #     print(op)
            # for op in insertion_operators:
            #     print(op)
            # print('\n')
                
            self.__update_weights(insertion_operators, insertion_weights)
            self.__update_weights(removal_operators, removal_weights)

        removal_operator_return = []
        insertion_operator_return = []

        for idx, op in enumerate(removal_operators):            
            removal_operator_return.append((op.name, removal_weights[idx]))
        for idx, op in enumerate(insertion_operators):
            insertion_operator_return.append((op.name, insertion_weights[idx]))

        return best_solutions, removal_operator_return, insertion_operator_return, itt_global
