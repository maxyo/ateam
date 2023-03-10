import json
import sys
from io import StringIO

from shapely import Point

from py.client.api.route import send_route
from py.client.models import Route, Move, SnowArea
from py.instance import client
from py.client.api.map_ import get_map
from py.config import HARDFILLED_BAGS, BAGS_COUNT, OUTPUT_PATH, IS_EVIL, PREPARED_MATRIX, SEND, TOKEN, MAP_ID, \
    MATRIX_SAVE_PATH, FIRST_SOLUTION_ALGORITHM, args
from py.evil import do_evil
from py.manybags import many_bags
from py.onebag import one_bag
from py.utils import get_distance, get_time_matrix, normalize_matrix, optimize_results
from py.vrp import vrp

def main():
    available_cost = 10000000
    used_cost = 0


    map_data = get_map.sync(client=client)
    map_data.gifts = map_data.gifts[0:len(map_data.children)]
    excluded = []

    bags = []
    for i in range(HARDFILLED_BAGS):
        res = one_bag(excluded, map_data.gifts)
        excluded.extend(res)
        bags.append(res)
        # add used cost calc

    bags.extend(list(many_bags(BAGS_COUNT - HARDFILLED_BAGS, excluded, map_data.gifts).values()))

    if PREPARED_MATRIX:
        with open(PREPARED_MATRIX, 'r') as f:
            matrix = json.load(f)
    else:
        matrix = get_time_matrix(map_data)

    if MATRIX_SAVE_PATH:
        io = StringIO()
        json.dump(matrix, io)
        with open(MATRIX_SAVE_PATH, "w") as f:
            f.writelines(io.getvalue())
    matrix = normalize_matrix(matrix)
    result = vrp({
        'distance_matrix': matrix,
        'bags': list(map(lambda i: len(i), bags))
    }, map_data)

    result['paths'] = optimize_results(result['paths'], map_data.snow_areas)
    result['totalMovements'] = len(result['paths'])

    result['bags'] = list(map(lambda i: {'total': len(i), 'items': i}, bags))

    result['config'] = {
        'algo': args.algo,
        'metaalgo': args.metaalgo,
        'hbcount': args.hbcount,
    }

    io = StringIO()
    json.dump(result, io)

    if IS_EVIL:
        do_evil(result)

    if OUTPUT_PATH == 'stdout':
        sys.stdout.write(io.getvalue())
    else:
        with open(OUTPUT_PATH, "w") as f:
            f.writelines(io.getvalue())

    if SEND:
        if not TOKEN:
            raise Exception('Token not found')
        result['bags'].reverse()
        route = Route(MAP_ID, list(map(lambda i: Move(i['x'], i['y']), result['paths'])),
                      list(map(lambda i: i['items'], result['bags'])))
        resp = send_route.sync_detailed(client=client, json_body=route)

        if resp.parsed:
            print('Successful sent %s' % resp.parsed.round_id if resp.parsed.success else resp.parsed.error)
        else:
            print(resp.status_code, resp.content)

if __name__ == '__main__':
    main()
