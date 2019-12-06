from instance import *
from solution import *
from queue import PriorityQueue
import random

class Simulation:

    def __init__(self, instance):
        self.instance = instance
        self.items = set(range(instance.number_items))
        self.current_solution = None


    def generate_random_solution(self):
        groups = []
        for i in range(self.instance.number_groups):
            lower_bound, upper_bound = self.instance.group_bounds[i]
            groups.append(Group(lower_bound, upper_bound))
        
        for i in self.items:
            included = False
            while not included:
                idx = random.choices(range(self.instance.number_groups))[0]
                included = groups[idx].add_item_if_viable(i, self.instance.adj_matrix[i])

        self.current_solution = Solution(self.instance.number_groups, self.instance.group_bounds, groups)

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
                evaluated_gains.put( ( ((-1) ** bestFirst) * group.evaluate_item(item, self.instance.adj_matrix[item]), i ) )
            
            while not added:
                _, group_index = evaluated_gains.get()
                added = groups[group_index].add_item_if_viable(item, self.instance.adj_matrix[item])
        
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
