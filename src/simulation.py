from instance import *
from solution import *
import random

class ALNS:

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
        for i in range(instance.num_items-1):
            for j in range(i+1, instance.num_items):
                pairs.append((i,j,instance.adj_matrix[i][j]))
        pairs.sort(key=lambda x: x[2])

        used_items = set()

        select_group = 0
        for i, j, k in pairs:
            if i not in used_items:
                if not groups[select_group].add_item_if_viable(i, self.instance.adj_matrix[i]):
                    select_group+=1

            if j not in used_items:
                if not groups[select_group].add_item_if_viable(j, self.instance.adj_matrix[j]):
                    select_group+=1
        for idx, group in enumerate(groups):
            if not group.is_valid():
                pass
                

    def local_search(self, solution):
        pass
        
