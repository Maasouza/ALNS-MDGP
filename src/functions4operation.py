from solution import *
import random

# Remoção aleatória
def removal_1(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)
        while number_of_removals > 0:
            item = random.choice(list(group.items))
            group.remove_item(item, instance.adj_matrix[item])
            removed_items.append(item)
            number_of_removals -= 1
    return removed_items

#TODO  Remoção aleatória enviesada
def removal_2(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)
        while number_of_removals > 0:
            item = solution.worst_item
            group.remove_item(item, instance.adj_matrix[item])
            removed_items.append(item)
            number_of_removals -= 1
    return removed_items

# Remoção gulosa pela menor contribuição
def removal_3(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)
        while number_of_removals > 0:
            item = solution.worst_item
            group.remove_item(item, instance.adj_matrix[item])
            removed_items.append(item)
            number_of_removals -= 1
    return removed_items

#TODO Remoção shaw
def removal_4(solution, instance, removal_rate):
    pass

def insertion_1(solution, instance, remaining_items):
    
    solution_groups = set(range(solution.num_groups))
    remaining_items = set(remaining_items)

    while len(remaining_items) > 0:
        item = random.sample(remaining_items,1)[0]
        included = False
        while not included and len(solution_groups) > 0:
            group_id = random.sample(solution_groups,1)[0]
            included = solution.groups[group_id].add_item_if_needed(item, instance.adj_matrix[item])
            if included:
                remaining_items.remove(item)
            else:
                solution_groups.remove(group_id)
        if len(solution_groups) == 0:
            break

    solution_groups = set(range(solution.num_groups))
    while len(remaining_items) > 0:
        item = random.sample(remaining_items,1)[0]
        included = False
        while not included:
            group_id = random.sample(solution_groups,1)[0]
            included = solution.groups[group_id].add_item_if_viable(item, instance.adj_matrix[item])
            if included:
                remaining_items.remove(item)
