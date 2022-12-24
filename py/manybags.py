from ortools.algorithms import pywrapknapsack_solver
from ortools.linear_solver import pywraplp

from py.client import Client, AuthenticatedClient
from py.client.api.map_ import get_map
from py.client.models import Gift
from py.config import client, BAGS_COUNT, WEIGHT_CAPACITY, VOLUME_CAPACITY
from py.utils import get_weight, get_volume, get_id


def many_bags(bags_count = BAGS_COUNT, excluded_gifts: list[int] = []):
    data = {}

    map_object = get_map.sync(client=client)
    gifts = map_object.gifts

    weights = {}
    volumes = {}
    items = {}

    for gift in gifts:
        try:
            excluded_gifts.index(gift.id)
        except:
            weights[gift.id] = gift.weight
            volumes[gift.id] = gift.volume
            items[gift.id] = gift.id

    bags = range(bags_count)

    data['weights'] = [
        48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36
    ]
    data['values'] = [
        10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25
    ]
    assert len(data['weights']) == len(data['values'])
    data['num_items'] = len(data['weights'])
    data['all_items'] = range(data['num_items'])

    data['bin_capacities'] = [100, 100, 100, 100, 100]
    data['num_bins'] = len(data['bin_capacities'])
    data['all_bins'] = range(data['num_bins'])

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

    # Objective.
    # Maximize total value of packed items.
    objective = solver.Objective()
    for i in items:
        for b in bags:
            objective.SetCoefficient(x[i, b], items[i])
    objective.SetMaximization()
    solver.set_time_limit(150000)
    status = solver.Solve()

    print(f'Total packed value: {objective.Value()}')
    total_weight = 0
    total_volume = 0
    min_count = 0
    max_count = len(gifts)
    packed = {}
    for b in bags:
        print(f'Bin {b}')
        packed[b] = []
        bin_weight = 0
        bin_volume = 0
        bin_value = 0
        for i in items:
            if x[i, b].solution_value() > 0:
                print(
                    f"Item {i} weight: {weights[i]} volume: {volumes[i]} value: {items[i]}"
                )
                packed[b].append(i)
                bin_weight += weights[i]
                bin_volume += volumes[i]
                bin_value += 1
        print(f'Packed bin weight: {bin_weight}')
        print(f'Packed bin volume: {bin_volume}\n')
        print(f'Packed bin value: {bin_value}\n')
        min_count = max(bin_value, min_count)
        max_count = min(bin_value, max_count)
        total_weight += bin_weight
        total_volume += bin_volume
    print(f'Total packed weight: {total_weight}')
    print(f'Total packed volume: {total_volume}')
    print(f'Min gifts at bin count: {min_count}')
    print(f'Max gifts at bin count: {max_count}')
    return []

