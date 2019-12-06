class Operator:
    def __init__(self):
        self.score = 0
        self.times_used = 0

    def increment(self, sigma):
        self.score += sigma

    def reset_score(self):
        self.score = 0


class InsertionOperator(Operator):
    def __init__(self, function):
        super()
        self.function = function

    def execute(self, partial_solution, remaining_items):
        # TODO: test if will change by ref
        self.times_used += 1
        self.function(partial_solution, remaining_items)

class RemovalOperator(Operator):
    def __init__(self, function):
        super()
        self.function = function

    def execute(self, partial_solution):
        # TODO: test if will change by ref
        self.times_used += 1
        return self.function(partial_solution) #removed items
