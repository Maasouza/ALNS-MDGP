class Group:
    
    def __init__(self, min_items, max_items):
        self.min_items = min_items
        self.max_items = max_items
        self.items = dict()
        self.num_items = len(self.items)
        self.obj_value = 0
        self.best_item = None
        self.worst_item = None

    def copy(self):
        min_items = self.min_items
        max_items = self.max_items
        
        new_group = Group(min_items, max_items)

        new_group.items = self.items.copy()
        
        new_group.num_items = self.num_items
        new_group.obj_value = self.obj_value
        
        new_group.best_item = self.best_item
        new_group.worst_item = self.worst_item
        
        return new_group

    def add_item_if_viable(self, item, item_diversity):
        if self.num_items + 1 <= self.max_items:
            return self.add_item(item, item_diversity)
        else:
            return False

    def add_item(self, item, item_diversity):
        max_contribution = -float('inf')
        min_contribution = float('inf')

        if item in self.items:
            return False
        item_contribution = 0
        for i in self.items:
            self.items[i] += item_diversity[i]
            
            self.update_best_and_worst(i, self.items[i], min_contribution, max_contribution)

            item_contribution += item_diversity[i] 
            
        self.update_best_and_worst(item, item_contribution, min_contribution, max_contribution)

        self.num_items += 1
        self.obj_value += item_contribution
        self.items[item] = item_contribution

        return True

    def evaluate_item(self, item, item_diversity):
        
        item_contribution = 0

        for i in self.items:
            item_contribution += item_diversity[i] 

        return float(item_contribution)/float(len(self.items))

    def remove_item_if_viable(self, item, item_diversity):
        if self.num_items - 1 >= self.min_items:
            return self.remove_item(item, item_diversity)
        else:
            return False

    def remove_item(self, item, item_diversity):
        max_contribution = -float('inf')
        min_contribution = float('inf')

        if item not in self.items:
            return False
        self.obj_value -= self.items[item]
        del self.items[item]
        self.num_items -= 1
        for i in self.items:
            self.items[i] -= item_diversity[i]
            self.update_best_and_worst(i, self.items[i], min_contribution, max_contribution)
        return True

    def is_valid(self):
        if self.num_items >= self.min_items and self.num_items <= self.max_items:
            return True
        else:
            return False

    def can_add_item(self):
        return self.num_items<self.max_items

    def update_best_and_worst(self, item, item_contribution, min_contribution, max_contribution):

        if item_contribution <= min_contribution :
                self.worst_item = item
        if item_contribution >= max_contribution :
                self.best_item = item

    def __repr__(self):
        return "("+str(self.min_items)+","+str(self.max_items)+")  -  ("+str(self.num_items)+")"