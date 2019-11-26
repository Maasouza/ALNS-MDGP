class Group:
    
    def __init__(self, min_items, max_items):
        
        self.min_items = min_items
        self.max_items = max_items
        self.items = dict()
        self.num_items = len(self.items)
        self.obj_value = 0

    def add_item_if_viable(self, item, item_diversity):
        if self.num_items + 1 <= self.max_items:
            return self.add_item(item, item_diversity)
        else:
            return False

    def add_item(self, item, item_diversity):
        if item in self.items:
            return False
        item_contribution = 0
        for i in self.items:
            self.items[i] += item_diversity[i]
            item_contribution += item_diversity[i] 
            
        self.num_items += 1
        self.obj_value += item_contribution
        self.items[item] = item_contribution
        return True

    def remove_item_if_viable(self, item, item_diversity):
        if self.num_items - 1 >= self.min_items:
            return self.remove_item(item, item_diversity)
        else:
            return False

    def remove_item(self, item, item_diversity):
        if item not in self.items:
            return False
        self.obj_value -= self.items[item]
        del self.items[item]
        self.num_items -= 1
        for i in self.items:
            self.items[i] -= item_diversity[i]
        return True

    def is_valid(self):
        if self.num_items >= self.min_items and self.num_items <= self.max_items:
            return True
        else:
            return False

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
        print("Groupos:")
        for idx, group in enumerate(self.groups):
            print("\tGrupo "+str(idx))
            print("\tDiversidade "+str(group.obj_value))
            print("\tContribuição individual")
            print("\t",group.items)
        return ""
