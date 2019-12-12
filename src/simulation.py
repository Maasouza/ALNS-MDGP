from instance import *
from solution import *
from utils import *
from queue import PriorityQueue
import random

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
            groups.append(Group(lower_bound, upper_bound))
        
        for item in self.items:
            included = False
            while not included:
                idx = random.choices(range(self.instance.number_groups))[0]
                included = groups[idx].add_item_if_viable(item, self.instance.adj_matrix[item])

        groups.sort(key = lambda x: x.min_items - x.num_items)
        for idx, group in enumerate(groups):
            if not group.is_valid():
                missing = groups[idx].min_items - groups[idx].num_items
                helper_idx = idx - 1
                while missing:
                    helper_item = groups[helper_idx].worst_item
                    if groups[helper_idx].remove_item_if_viable(helper_item, self.instance.adj_matrix[helper_item]):
                        groups[idx].add_item_if_viable(helper_item, self.instance.adj_matrix[helper_item])
                        missing -= 1
                    else:
                        helper_idx -= 1

        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_1(self):
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(lower_bound, upper_bound))

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
        
        groups.sort(key = lambda x: x.min_items - x.num_items)
        for idx, group in enumerate(groups):
            if not group.is_valid():
                missing = groups[idx].min_items - groups[idx].num_items
                helper_idx = idx - 1
                while missing:
                    helper_item = groups[helper_idx].worst_item
                    if groups[helper_idx].remove_item_if_viable(helper_item, self.instance.adj_matrix[helper_item]):
                        groups[idx].add_item_if_viable(helper_item, self.instance.adj_matrix[helper_item])
                        missing -= 1
                    else:
                        helper_idx -= 1
        
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_2(self):

        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(lower_bound, upper_bound))

        mean_diversity = []
        for item, item_diversity in enumerate(self.instance.adj_matrix):
            mean_diversity.append( (item, sum(item_diversity) / float( len(item_diversity) - 1) ) )

        mean_diversity.sort(key=lambda x:x[1], reverse = True) 
       
        select_group = 0
        for i, _ in mean_diversity:
            while not groups[select_group].add_item_if_viable(i, self.instance.adj_matrix[i]):
               select_group+=1
            
        groups.sort(key = lambda x: x.min_items - x.num_items)
        for idx, group in enumerate(groups):
            if not group.is_valid():
                missing = groups[idx].min_items - groups[idx].num_items
                helper_idx = idx - 1
                while missing:
                    helper_item = groups[helper_idx].worst_item
                    if groups[helper_idx].remove_item_if_viable(helper_item, self.instance.adj_matrix[helper_item]):
                        groups[idx].add_item_if_viable(helper_item, self.instance.adj_matrix[helper_item])
                        missing -= 1
                    else:
                        helper_idx -= 1
        
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def greedy_solution_3(self, bestFirst):
        
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(lower_bound, upper_bound))

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
        
        groups.sort(key = lambda x: x.min_items - x.num_items)
        for idx, group in enumerate(groups):
            if not group.is_valid():
                missing = groups[idx].min_items - groups[idx].num_items
                helper_idx = idx - 1
                while missing:
                    helper_item = groups[helper_idx].worst_item
                    if groups[helper_idx].remove_item_if_viable(helper_item, self.instance.adj_matrix[helper_item]):
                        groups[idx].add_item_if_viable(helper_item, self.instance.adj_matrix[helper_item])
                        missing -= 1
                    else:
                        helper_idx -= 1
        
        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)
        if self.best_solution is None or self.current_solution > self.best_solution:
            self.best_solution = self.current_solution.copy()


    def __update_weights(self, operators, weights, r=0.8):
        for idx, operator in enumerate(operators):
            try:
                weights[idx] = weights[idx] * (1-r) + r * (operator.score/operator.times_used)
            except ZeroDivisionError:
                pass
            operator.reset_score()
            operator.reset_times_used()


    def alns(self, max_itts, initial_temperature, final_temperature, insertion_operators, removal_operators, removal_rate=0.3):
        current_temperature = initial_temperature

        removal_weights = [ 1.0 ] * len(removal_operators) 
        insertion_weights = [ 1.0 ] * len(insertion_operators) 
        
        while current_temperature >= final_temperature:
            itt = 0

            while itt < max_itts:
                new_solution = self.current_solution.copy()
                
                removal_operator = roulette(removal_operators, removal_weights)
                removed_items = removal_operator.execute(new_solution, self.instance, removal_rate)
                new_solution.update_obj_value()

                insertion_operator = roulette(insertion_operators, insertion_weights)
                insertion_operator.execute(new_solution, self.instance, removed_items)
                new_solution.update_obj_value()
                

                #TODO adicionar soluções ao path relink soluções
                if new_solution > self.current_solution:
                    self.current_solution = new_solution.copy()
                    if self.current_solution > self.best_solution:
                        self.best_solution = self.current_solution.copy()
                        # sigma_1 points
                        sigma_1 = 1.0
                        removal_operator.increment(sigma_1)
                        insertion_operator.increment(sigma_1)
                    else:
                        # sigma_2 points
                        sigma_2 = 0.5
                        removal_operator.increment(sigma_2)
                        insertion_operator.increment(sigma_2)
                else:
                    delta_solution = new_solution.obj_value - self.current_solution.obj_value
                    # accepted by simulated annealing criteria
                    if random.random() < boltzman(delta_solution, current_temperature):
                        self.current_solution = new_solution.copy()
                        # sigma_3 points
                        sigma_3 = 0.2
                        removal_operator.increment(sigma_3)
                        insertion_operator.increment(sigma_3)
                itt += 1
            
            current_temperature *= 0.9 # cooling
            
            for op in removal_operators:
                print(op)
            for op in insertion_operators:
                print(op)
            print('\n')
                
            self.__update_weights(insertion_operators, insertion_weights)
            self.__update_weights(removal_operators, removal_weights)
