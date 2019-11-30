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
