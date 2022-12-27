from ortools.linear_solver import pywraplp

from py.client.models import Gift
from py.config import BAGS_COUNT, WEIGHT_CAPACITY, VOLUME_CAPACITY, MANY_BAGS_FINDING_TIME_LIMIT_MS, \
    ENABLE_DEBUG


def many_bags(bags_count = BAGS_COUNT, excluded_gifts: list[int] = [], gifts: list[Gift] =[], available_cost = 10000):
    weights = {}
    volumes = {}
    costs = {}
    items = {}

    for gift in gifts:
        try:
            excluded_gifts.index(gift.id)
        except:
            weights[gift.id] = gift.weight
            volumes[gift.id] = gift.volume
            items[gift.id] = gift.id
            costs[gift.id] = 1

    bags = range(bags_count)

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print('SCIP solver unavailable.')
        return

    # Variables.
    # x[i, b] = 1 if item i is packed in bin b.
    x = {}
    for i in items:
        for b in bags:
            x[i, b] = solver.BoolVar(f'x_{i}_{b}')

    # Constraints.
    # Each item is assigned to at most one bin.
    for i in items:
        solver.Add(sum(x[i, b] for b in bags) <= 1)

    # The amount packed in each bin cannot exceed its capacity.
    for b in bags:
        solver.Add(
            sum(x[i, b] * weights[i]
                for i in items) <= WEIGHT_CAPACITY)
    # The amount packed in each bin cannot exceed its capacity.
    for b in bags:
        solver.Add(
            sum(x[i, b] * volumes[i]
                for i in items) <= VOLUME_CAPACITY)
    solver.Add(sum(x[i, b] * costs[i] for i in items for b in bags) <= available_cost)

    # Objective.
    # Maximize total value of packed items.
    objective = solver.Objective()
    for i in items:
        for b in bags:
            objective.SetCoefficient(x[i, b], items[i])
    objective.SetMaximization()
    solver.set_time_limit(MANY_BAGS_FINDING_TIME_LIMIT_MS)
    status = solver.Solve()

    ENABLE_DEBUG and print(f'Total packed value: {objective.Value()}')
    total_weight = 0
    total_volume = 0
    min_count = 0
    max_count = len(gifts)
    packed = {}
    for b in bags:
        ENABLE_DEBUG and print(f'Bin {b}')
        packed[b] = []
        bin_weight = 0
        bin_volume = 0
        bin_value = 0
        for i in items:
            if x[i, b].solution_value() > 0:
                ENABLE_DEBUG and print(
                    f"Item {i} weight: {weights[i]} volume: {volumes[i]} value: {items[i]}"
                )
                packed[b].append(i)
                bin_weight += weights[i]
                bin_volume += volumes[i]
                bin_value += 1
        ENABLE_DEBUG and print(f'Packed bin weight: {bin_weight}')
        ENABLE_DEBUG and print(f'Packed bin volume: {bin_volume}\n')
        ENABLE_DEBUG and print(f'Packed bin value: {bin_value}\n')
        min_count = max(bin_value, min_count)
        max_count = min(bin_value, max_count)
        total_weight += bin_weight
        total_volume += bin_volume
    ENABLE_DEBUG and print(f'Total packed weight: {total_weight}')
    ENABLE_DEBUG and print(f'Total packed volume: {total_volume}')
    ENABLE_DEBUG and print(f'Min gifts at bin count: {min_count}')
    ENABLE_DEBUG and print(f'Max gifts at bin count: {max_count}')
    return packed

