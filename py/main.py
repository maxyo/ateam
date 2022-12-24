import json
import sys
from io import StringIO

from py.client.api.map_ import get_map
from py.config import client, HARDFILLED_BAGS, BAGS_COUNT, OUTPUT_PATH
from py.manybags import many_bags
from py.onebag import one_bag
from py.utils import get_distance_matrix
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
    result = vrp({
        'distance_matrix': get_distance_matrix(map_data),
        'bags': list(map(lambda i: len(i), bags))
    }, map_data)

    result['bags'] = list(map(lambda i: {'total': len(i), 'items': i}, bags))

    io = StringIO()
    json.dump(result, io)


    if OUTPUT_PATH == 'stdout':
        sys.stdout.write(io.getvalue())
    else:
        with open(OUTPUT_PATH, "w") as f:
            f.writelines(io.getvalue())


if __name__ == '__main__':
    main()
