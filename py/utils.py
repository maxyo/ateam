import copy
import json
import math
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Pool

import matplotlib
import multithreading
import shapely
from matplotlib.pyplot import plot, show, figure

from py.client.models import Gift, Map, Child, SnowArea
from py.config import SPEED, SNOWSTORM_SPEED
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
    areaP = Point(area.x, area.y)

    if len(intersect) == 0:
        return [source, target]

    if (len(intersect)) == 2:
        source_to_area_dist = get_distance(intersect[0], areaP)
        source_to_target_dist = get_distance(intersect[0], intersect[1])
        area_to_target_dist = get_distance(areaP, intersect[1])

        source_cos = get_cos(source_to_target_dist, source_to_area_dist, area_to_target_dist)
        target_cos = get_cos(source_to_target_dist, area_to_target_dist, source_to_area_dist)
        area_cos = get_cos(area_to_target_dist, source_to_area_dist, source_to_target_dist)

        source_sin = get_sin(source_cos)
        target_sin = get_sin(target_cos)
        area_sin = get_sin(area_cos)

        source_radians = math.acos(source_cos)
        target_radians = math.acos(target_cos)
        area_radians = math.acos(area_cos)

        if source_radians == target_radians:
            target_radians = -target_radians

        left_radians = area_radians

        distance = (math.pi*area.r/180)*math.degrees(left_radians)

        steps = int(distance+50)
        new_points = []
        for i in range(steps + 1):
            radian = lerp(source_radians, target_radians, i/steps)

            # new_points.append(Point(math.sin(radian)*area.r + area.x, math.cos(radian)*area.r + area.y))
            new_points.append(Point(math.sin(radian)*area.r, math.cos(radian)*area.r))


        path = []

        prev = new_points[0]

        for step in new_points:
            if step == prev:
                continue
            path.append([prev, step, False])
            prev = step

        d = get_time_for_hard_path(path) * SPEED
        f = figure(figsize=(2,2))
        plot(list(map(lambda i: i.x, new_points)), list(map(lambda i: i.y, new_points)))
        show()
        return


    pass


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
    for area in snowAreas:
        points = get_intersect_points(pointA, pointB, area)
        if len(points) > 0:
            path.append([lastPoint, points[0], False])
            if len(points) == 1:  # target inside area
                path.append([points[0], pointB, True])
                lastPoint = pointB
            else:
                path.append([points[0], points[1], True])
                lastPoint = points[1]
        else:
            continue

    if lastPoint != pointB:
        path.append([lastPoint, pointB, False])

    return get_time_for_hard_path(path)


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
        print('Done %s' % str(id))
        json.dump(res[1], f)


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
