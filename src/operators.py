class Operator:
    def __init__(self, name, op_type):
        self.score = 0
        self.times_used = 0
        self.name = name
        self.op_type = op_type

    def increment(self, sigma):
        self.score += sigma

    def reset_score(self):
        self.score = 0
    
    def reset_times_used(self):
        self.times_used = 0

    def __repr__(self):
        return self.op_type + ' - ' + self.name + ':\n Score: ' + str(self.score) + ' - Times Used: ' + str(self.times_used)

class InsertionOperator(Operator):
    def __init__(self, function, name):
        Operator.__init__(self, name, 'Insertion Operator')
        self.function = function

    def execute(self, partial_solution, instance, remaining_items):
        self.times_used += 1
        self.function(partial_solution, instance, remaining_items)

class RemovalOperator(Operator):
    def __init__(self, function, name):
        Operator.__init__(self, name, 'Removal Operator')
        self.function = function

    def execute(self, partial_solution, instance, removal_rate):
        self.times_used += 1
        return self.function(partial_solution, instance, removal_rate) #removed items
