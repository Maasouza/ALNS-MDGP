from group import *

class Solution:

    def __init__(self, num_groups, groups_bounds, groups = [], obj_value = 0):
        self.num_groups = num_groups
        self.groups = groups
        self.obj_value = obj_value
        if groups == []:
            for min_items, max_items in groups_bounds :
                self.groups.append(Group(min_items, max_items))
        else:
            self.update_obj_value()

    def update_obj_value(self):
        self.obj_value = 0
        for group in self.groups:
            self.obj_value += group.obj_value
        
    def is_valid_solution(self):
        valid_groups = 1
        for group in self.groups:
            valid_groups *= group.is_valid()
        return valid_groups

    def __repr__(self):
        print("Diversidade ", self.obj_value)
        # print("Groupos:")
        # for idx, group in enumerate(self.groups):
        #     print("\tGrupo "+str(idx))
        #     print("\tDiversidade "+str(group.obj_value))
        #     print("\tContribuição individual")
        #     print("\t",group.items)
        return ""
