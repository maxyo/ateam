"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from py.client.models import Map
from py.config import WEIGHT_CAPACITY, BAGS_COUNT, ENABLE_DEBUG


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(BAGS_COUNT):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for run {} (available gifts {}):\n'.format(vehicle_id, data['bags'][vehicle_id])
        route_distance = 0
        children = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            plan_output += ' {0} ->'.format(node_index)
            if node_index != 0:
                children += 1
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}\n'.format(route_distance)
        plan_output += 'Children at the route: {}\n'.format(children)
        print(plan_output)
        total_distance += route_distance
    print('Total distance of all routes: {}m'.format(total_distance))


def vrp(data, map: Map):
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        BAGS_COUNT,
        0)
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'

    # Add Capacity constraint.
    def bag_size_callback(from_index, to_index):
        if (manager.IndexToNode(from_index) == 0):
            return 0
        return 1

    bag_size_callback_index = routing.RegisterTransitCallback(
        bag_size_callback)
    routing.AddDimensionWithVehicleCapacity(
        bag_size_callback_index,
        0,  # null capacity slack
        data['bags'],
        False,
        'Bag size')
    # routing.AddDimension(
    #     transit_callback_index,
    #     0,  # no slack
    #     300000,  # vehicle maximum travel distance
    #     True,  # start cumul to zero
    #     dimension_name)
    # distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.time_limit.seconds = 25

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        if ENABLE_DEBUG:
            print_solution(data, manager, routing, solution)
            print(f'Objective: {solution.ObjectiveValue()}')

        total_distance = 0

        paths = []
        for vehicle_id in range(BAGS_COUNT):
            index = routing.Start(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
                paths.append(
                    {'x': map.children[node_index - 1].x, 'y': map.children[node_index - 1].y} if node_index != 0 else {
                        'x': 0, 'y': 0})
            total_distance += route_distance
        return {
            'totalDistance': 0,
            'totalTime': 0,
            'totalMovements': 0,
            'paths': paths
        }

    else:
        print('No solution found !')
