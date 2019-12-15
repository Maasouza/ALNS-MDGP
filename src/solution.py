from group import *

class Solution:

    def __init__(self, num_groups, groups_bounds = None, groups = [], obj_value = 0):
        self.num_groups = num_groups
        self.groups = groups
        self.obj_value = obj_value
        if groups == []:
            for idx, min_items, max_items in enumerate(groups_bounds) :
                self.groups.append(Group(idx, min_items, max_items))
        else:
            self.update_obj_value()


    def copy(self):
        num_groups = self.num_groups
        groups = []

        for group in self.groups:
            groups.append(group.copy()) 

        return Solution(num_groups, groups=groups) 

    def update_obj_value(self):
        self.obj_value = 0
        for group in self.groups:
            self.obj_value += group.obj_value

        self.obj_value = round(self.obj_value, 3)
        
    def is_valid_solution(self):
        valid_groups = 1
        for group in self.groups:
            valid_groups *= group.is_valid()
        return valid_groups

    def __repr__(self):
        print("Diversidade ", self.obj_value)
        print("Viavél ", self.is_valid_solution())
        # print("Groupos:")
        # for idx, group in enumerate(self.groups):
        #     print("\tGrupo "+str(idx))
        #     print("\tDiversidade "+str(group.obj_value))
        #     print("\tContribuição individual")
        #     print("\t",group.items)
        return ""
    
    def __eq__(self, other):
        return self.obj_value == other.obj_value
    
    def __gt__(self, other):
        return self.obj_value > other.obj_value
    
    def __ge__(self, other):
        return self.obj_value >= other.obj_value
