import copy
import json
import math
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Pool

import matplotlib
import multithreading
import shapely
from matplotlib.pyplot import plot, show, figure

from py.circle_around import get_points_outside
from py.client.models import Gift, Map, Child, SnowArea
from py.config import SPEED, SNOWSTORM_SPEED, ENABLE_DEBUG
from shapely.geometry import LineString
from shapely.geometry import Point


def get_weight(gift: Gift):
    return gift.weight


def get_volume(gift: Gift):
    return gift.volume


def get_id(gift: Gift):
    return gift.id


def get_distance(pointA: Point, pointB: Point):
    return abs(math.sqrt(
        math.pow(pointB.y - pointA.y, 2)
        + math.pow(pointB.x - pointA.x, 2)
    ))


def get_intersect_points(pointA: Point, pointB: Point, area: SnowArea):
    from shapely.geometry import LineString
    from shapely.geometry import Point

    p = Point(area.x, area.y)
    c = p.buffer(area.r).boundary
    l = LineString([pointA, pointB])
    i = c.intersection(l)

    if i.geom_type == 'Point':
        return [i]

    return list(i.geoms) if not i.is_empty else []


def get_cos(a, b, c):
    return (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def get_sin(cos):
    return math.sqrt(1 - cos**2)
def optimized_path(source: Point, target: Point, area: SnowArea):
    intersect = get_intersect_points(source, target, area)
    if (len(intersect)) == 2:
        points = []
        get_points_outside(points, area.x, area.y, area.r, intersect[0].x, intersect[0].y, intersect[1].x, intersect[1].y)

        points = list(map(lambda i: Point(i[0], i[1]), points))


        return points

    if(len(intersect) == 1):
        pass

    return []

def optimized_path_withsloments(source: Point, target: Point, area: SnowArea):
    intersect = get_intersect_points(source, target, area)
    if (len(intersect)) == 2:
        points = []
        get_points_outside(points, area.x, area.y, area.r, intersect[0].x, intersect[0].y, intersect[1].x, intersect[1].y)

        points = list(map(lambda i: Point(i[0], i[1]), points))

        path = []

        prev = points[0]
        last = points[0]
        for p in points:
            if p == prev:
                continue
            path.append([prev, p, False])
            prev = p

        return path

    if(len(intersect) == 1):
        return [
            [source, intersect[0], False],
            [intersect[0], target, True],
        ]
        pass

    return [[source, target, False]]


def get_time_for_hard_path(paths: list):
    total_fast_distance = 0
    total_slow_distance = 0

    for p in paths:
        p1 = p[0]
        p2 = p[1]
        is_slow = p[2]

        if is_slow:
            total_slow_distance += get_distance(p1, p2)
        else:
            total_fast_distance += get_distance(p1, p2)

    return (total_slow_distance / SNOWSTORM_SPEED) + (total_fast_distance / SPEED)


def sort_func_area(sourcePoint: Point):
    def func(area: SnowArea):
        return get_distance(Point(area.x, area.y), sourcePoint)

    return func


def get_time(pointA: Point, pointB: Point, snowAreas: list[SnowArea]):
    path = []

    lastPoint = pointA

    if pointB.y == pointA.y and pointB.x == pointA.x:
        return 0


    snowAreas.sort(key=sort_func_area(pointA))

    optimized = optimize_path([pointA, pointB], snowAreas)
    optimized.insert(0, [pointA, optimized[0][0], False])
    optimized.append([optimized[-1][1], pointB, False])

    optimized_time = get_time_for_hard_path(optimized)
    direct_time = get_time_for_hard_path([[pointA, pointB, False]])


    return min(direct_time, optimized_time)


def normalize_matrix(matrix):
    max_decimals = 0

    for it in matrix:
        for it2 in it:
            max_decimals = max(str(it2)[::-1].find('.'), max_decimals)

    mul = 10 ** max_decimals

    for it in matrix:
        for i in range(len(it)):
            it[i] = int(it[i])

    return matrix


def calc(id, snow_areas, children):
    res = []
    for i2 in range(len(children)):
        res.append(
            get_time(Point(children[id].x, children[id].y), Point(children[i2].x, children[i2].y),
                     snow_areas))
    return [id, res]


def task(id, areas, children):
    res = calc(id, areas, children)
    with open('/tmp/%s.json' % id, 'w') as f:
        ENABLE_DEBUG and print('Done %s' % str(id))
        json.dump(res[1], f)


def optimize_results(moves, snowAreas: list[SnowArea]):
    result = []
    prev = moves[0]
    prevpoint = Point(moves[0]['x'], moves[0]['y'])
    last = moves[0]
    for move in moves:
        last = move
        movepoint = Point(move['x'], move['y'])
        if move == prev:
            continue

        snowAreas.sort(key=sort_func_area(prevpoint))

        result.append(prev)

        for area in snowAreas:
            op = optimized_path(prevpoint, movepoint, area)

            for p in op:
                result.append({'x': int(p.x), 'y': int(p.y)})
                prevpoint = p


        prevpoint = Point(move['x'], move['y'])
        prev = move

    result.append(last)

    return result

def optimize_path(moves, snowAreas: list[SnowArea]):
    result = []
    prev = moves[0]
    last = moves[0]
    for move in moves:
        last = move
        movepoint = move
        if move == prev:
            continue

        snowAreas.sort(key=sort_func_area(prev))

        result.append([prev, move, False])

        for area in snowAreas:
            op = optimized_path_withsloments(prev, movepoint, area)

            for p in op:
                result.append(p)
                prev = p[1]

        prev = move

    result.append([prev, last, False])

    return result

def get_time_matrix(map: Map):
    children = copy.copy(map.children)
    children.insert(0, Child(0, 0))

    targets = {}

    # warehouse

    pool = Pool()
    processes = []
    for i in range(len(children)):
        p = pool.apply_async(task, (i, copy.copy(map.snow_areas), children))
        processes.append(p)

    for p in processes:
        p.get()

    # print(targets)
    collected = []

    for i in range(len(children)):
        with open('/tmp/%s.json' % i, 'r') as f:
            res = json.load(f)
            collected.append(res)

    result = collected

    # for i in range(len(children)):
    #     target = []
    #     result.append(target)
    #     for i2 in range(len(children)):
    #         target.append(
    #             get_time(Point(children[i].x, children[i].y), Point(children[i2].x, children[i2].y), map.snow_areas))

    return result
