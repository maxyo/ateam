import json
import sys
from io import StringIO

from py.instance import client
from py.client.api.map_ import get_map
from py.config import HARDFILLED_BAGS, BAGS_COUNT, OUTPUT_PATH, IS_EVIL
from py.evil import do_evil
from py.manybags import many_bags
from py.onebag import one_bag
from py.utils import get_distance_matrix, get_distance, get_time_matrix
from py.vrp import vrp


def main():
    map_data = get_map.sync(client=client)
    excluded = []

    bags = []
    for i in range(HARDFILLED_BAGS):
        res = one_bag(excluded)
        excluded.extend(res)
        bags.append(res)

    bags.extend(list(many_bags(BAGS_COUNT - HARDFILLED_BAGS, excluded).values()))
    matrix = get_time_matrix(map_data)
    io = StringIO()
    json.dump(matrix, io)
    with open('./data.json', "w") as f:
        f.writelines(io.getvalue())

    result = vrp({
        'distance_matrix': matrix,
        'bags': list(map(lambda i: len(i), bags))
    }, map_data)

    result['bags'] = list(map(lambda i: {'total': len(i), 'items': i}, bags))

    io = StringIO()
    json.dump(result, io)

    if IS_EVIL:
        do_evil(result)

    if OUTPUT_PATH == 'stdout':
        sys.stdout.write(io.getvalue())
    else:
        with open(OUTPUT_PATH, "w") as f:
            f.writelines(io.getvalue())


if __name__ == '__main__':
    main()
