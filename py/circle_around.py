#!/usr/bin/python3.10

import math
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

from turtle import Vec2D
from shapely.geometry import LineString
from shapely.geometry import Point


def rotate2D(angle, x0, y0, x1, y1):
    """Rotate (x0, y0) -> (x1, y1) vector by *angle*."""
    x, y = Vec2D(x1 - x0, y1 - y0).rotate(angle)
    return x + x0, y + y0


def get_intersect(cx, cy, cr, x0, y0, x1, y1):
    p = Point(cx, cy)
    circle = p.buffer(cr).boundary
    line = LineString([(x0, y0), (x1, y1)])
    intersection = circle.intersection(line)
    points = []
    if intersection:
        for geom in intersection.geoms:
            points.append(geom.coords[0])
        return points
    else:
        return False


def get_cos(a, b, c):
    return (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)


def get_distance(x0, y0, x1, y1):
    return abs(math.sqrt(
        math.pow(y0 - y1, 2)
        + math.pow(x0 - x1, 2)
    ))


# Находит точку за пределами окружности, которая позволяет обойти окружность по кратчайшему пути
def get_points_outside(points, cx, cy, cr, x0, y0, x1, y1):
    source_to_area_dist = round(get_distance(x0, y0, cx, cy), 2)
    source_to_target_dist = round(get_distance(x0, y0, x1, y1), 2)
    area_to_target_dist = round(get_distance(cx, cy, x1, y1), 2)

    area_cos = round(get_cos(area_to_target_dist, source_to_area_dist, source_to_target_dist), 2)
    area_radians = math.acos(area_cos)
    distance = (math.pi * cr / 180) * math.degrees(area_radians)
    count = max(math.ceil(distance / 20), 2)
    h = dist([x0, y0], [x1, y1])
    rad = 180 / math.pi
    a = math.asin(h / 2 / cr) * 2 * rad
    [xe, ye] = rotate2D(a, cx, cy, x0, y0)
    [xs, ys] = rotate2D(-a, cx, cy, x0, y0)
    if round(xs/10, 0)*10 == round(x1/10, 0)*10 and round(ys/10, 0)*10 == round(y1/10, 0)*10:
        a = -a
    da = a / (count - 1)

    vec = Point(cx - x0, cy - y0)

    if vec.x > 0:
        x0 -= 2
    else:
        x0 += 2

    if vec.y > 0:
        y0 -= 2
    else:
        y0 += 2

    points.append([int(x0), int(y0)])
    xi = x0
    yi = y0
    for i in range(count - 1):
        angle = da * (i + 1)
        [xi, yi] = rotate2D(da, cx, cy, xi, yi)

        vec = Point(cx - xi, cy - yi)

        resx = xi
        resy = yi
        if vec.x > 0:
            resx -= 2
        else:
            resx += 2

        if vec.y > 0:
            resy -= 2
        else:
            resy += 2

        points.append([int(resx), int(resy)])
    vec = Point(cx - x1, cy - y1)

    if vec.x > 0:
        x1 -= 2
    else:
        x1 += 2

    if vec.y > 0:
        y1 -= 2
    else:
        y1 += 2

    points.append([int(x1), int(y1)])
    return points


def dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Строит маршрут огибания бури
# cx - X coordinate of circle`s center
# cy - Y coordinate of circle`s center
# cr - radius of circle
# x0, y0 - coordinates of first point
# x1, y1 - coordinates of second point
# return [[x0,y0],[x1,y1],...,[xn,yn]] - array of points, includes start and end points of route

# print(i.geoms[0].coords[0])
# print(i.geoms[1].coords[0])
