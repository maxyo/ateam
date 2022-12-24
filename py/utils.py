import copy
import math

from py.client.models import Gift, Map, Child


def get_weight(gift: Gift):
    return gift.weight


def get_volume(gift: Gift):
    return gift.volume


def get_id(gift: Gift):
    return gift.id


def get_distance(pointA: Child, pointB: Child, map: Map):
    return math.floor(abs(math.sqrt(
        math.pow(pointB.y - pointA.y, 2)
        + math.pow(pointB.x - pointA.x, 2)
    )))


def get_distance_matrix(map: Map):
    result = []

    children = copy.copy(map.children)

    # warehouse

    children.insert(0, Child(0, 0))

    for i in range(len(children)):
        target = []
        result.append(target)
        for i2 in range(len(children)):
            target.append(get_distance(children[i], children[i2], map))

    return result
