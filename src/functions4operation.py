from solution import *
import random
import numpy as np

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

# Remoção aleatória enviesada
def removal_2(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)
        items = list(solution.items)

        prob_items = []
        for item in items:
            prob_items.append(1.0/solution.items[item])
        
        sum_prob = sum(prob_items)
        
        for item in range(len(items)):
            prob_items[item] /= sum_prob
        
        for item in np.random.choice(items, number_of_removals, p=prob_items):
            group.remove_item(item, diversity_matrix[item])
            removed_items.append(item)

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

# Remoção shaw
def removal_4(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)
        while number_of_removals > 0:
            item = random.choice(list(group.items))
            
            similar_item = None
            max_similarity = 0
            for k in group.items:
                if k != item and instance.similarity_matrix[item][k] > max_similarity:
                    max_similarity = instance.similarity_matrix[item][k]
                    similar_item = k

            group.remove_item(item, instance.adj_matrix[item])
            group.remove_item(similar_item, instance.adj_matrix[similar_item])
            removed_items.extend([item, similar_item])
            number_of_removals -= 2
    return removed_items

# Remoção shaw 2
def removal_5(solution, instance, removal_rate):
    removed_items = []
    for group in solution.groups:
        number_of_removals = round(group.num_items*removal_rate)

        item = random.choice(list(group.items))
        
        max_similarity = []
        for k in group.items:
            if k != item and instance.similarity_matrix[item][k] > max_similarity:
                max_similarity.append((k, instance.similarity_matrix[item][k]))

        max_similarity.sort(key=lambda x: x[1])            

        group_removals = max_similarity[:number_of_removals]

        for item_removal, _ in group_removals:
            group.remove_item(item_removal, instance.adj_matrix[item_removal])
            removed_items.append(item_removal)
    return removed_items

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
