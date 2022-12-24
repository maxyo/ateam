from ortools.algorithms import pywrapknapsack_solver

from py.client import Client, AuthenticatedClient
from py.client.api.map_ import get_map
from py.client.models import Gift

WEIGHT_CAPACITY = 200
VOLUME_CAPACITY = 100

url = 'https://datsanta.dats.team'

def get_weight(gift: Gift):
    return gift.weight

def get_volume(gift: Gift):
    return gift.volume
def get_id(gift: Gift):
    return gift.id

def main():
    client = Client(base_url=url)
    map_object = get_map.sync(client=client)
    gifts = map_object.gifts


    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    values = list(map(get_id, gifts))
    weights = [list(map(get_weight, gifts)), list(map(get_volume, gifts))]
    capacities = [WEIGHT_CAPACITY, VOLUME_CAPACITY]

    solver.Init(values, weights, capacities)
    solver.set_time_limit(60)

    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)
    print('Packed items:', packed_items)
    print('Packed_weights:', packed_weights)


if __name__ == '__main__':
    main()
