import copy
import math

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
    return math.floor(abs(math.sqrt(
        math.pow(pointB.y - pointA.y, 2)
        + math.pow(pointB.x - pointA.x, 2)
    )))


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

    return math.ceil(get_time_for_hard_path(path))


def get_time_matrix(map: Map):
    result = []

    children = copy.copy(map.children)

    # warehouse

    children.insert(0, Child(0, 0))

    for i in range(len(children)):
        target = []
        result.append(target)
        for i2 in range(len(children)):
            target.append(
                get_time(Point(children[i].x, children[i].y), Point(children[i2].x, children[i2].y), map.snow_areas))

    return result


def get_distance_matrix(map: Map):
    result = []

    children = copy.copy(map.children)

    # warehouse

    children.insert(0, Child(0, 0))

    for i in range(len(children)):
        target = []
        result.append(target)
        for i2 in range(len(children)):
            target.append(get_distance(Point(children[i].x, children[i].y), Point(children[i2].x, children[i2].y)))

    return result
