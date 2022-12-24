from ortools.algorithms import pywrapknapsack_solver

from py.client.api.map_ import get_map
from py.config import client, VOLUME_CAPACITY, WEIGHT_CAPACITY
from py.utils import get_weight, get_id, get_volume




def one_bag(excluded_gifts: list[int] = []):
    map_object = get_map.sync(client=client)
    raw_gifts = map_object.gifts

    gifts = []

    for gift in raw_gifts:
        try:
            excluded_gifts.index(gift.id)
        except:
            gifts.append(gift)



    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'KnapsackExample')
    values = list(map(get_id, gifts))
    weights = [list(map(get_weight, gifts)), list(map(get_volume, gifts))]
    capacities = [WEIGHT_CAPACITY, VOLUME_CAPACITY]

    solver.Init(values, weights, capacities)

    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    packed_volumes = []
    total_weight = 0
    total_volume = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(values[i])
            packed_weights.append(weights[0][i])
            packed_volumes.append(weights[1][i])
            total_weight += weights[0][i]
            total_volume += weights[1][i]
    print('Total items:', len(packed_items))
    print('Total weight:', total_weight)
    print('Total volume:', total_volume)
    print('Packed items:', packed_items)
    print('Packed volumes:', packed_volumes)
    print('Packed_weights:', packed_weights)

    return packed_items

