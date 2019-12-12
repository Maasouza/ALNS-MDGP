class Operator:
    def __init__(self):
        self.score = 0
        self.times_used = 0

    def increment(self, sigma):
        self.score += sigma

    def reset_score(self):
        self.score = 0
    
    def reset_times_used(self):
        self.times_used = 0


class InsertionOperator(Operator):
    def __init__(self, function):
        Operator.__init__(self)
        self.function = function

    def execute(self, partial_solution, diversities_matrix, remaining_items):
        self.times_used += 1
        self.function(partial_solution, diversities_matrix, remaining_items)

class RemovalOperator(Operator):
    def __init__(self, function):
        Operator.__init__(self)
        self.function = function

    def execute(self, partial_solution, diversities_matrix, removal_rate):
        self.times_used += 1
        return self.function(partial_solution, diversities_matrix, removal_rate) #removed items
