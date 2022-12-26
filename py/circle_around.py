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


# Находит точку за пределами окружности, которая позволяет обойти окружность по кратчайшему пути
def get_points_outside(points, cx, cy, cr, x0, y0, x1, y1, count=20):
    h = dist([x0, y0], [x1, y1])
    print("Dist: ", h, h / 2 / cr)
    rad = 180 / math.pi;
    a = math.asin(h / 2 / cr) * rad * 2;
    da = a / count;
    points.append([x0, y0])
    for i in range(count - 1):
        # [xi, yi] = rotate2D(da * (i + 1), cx, cy, x0, y0)
        [xi, yi] = rotate2D(da * (i + 1), cx, cy, x0, y0)
        points.append([xi, yi])
        print(xi, yi)

    points.append([x1, y1])
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
def get_route(cx,cy,cr, x0, y0, x1, y1):
    i = get_intersect(cx,cy,cr, x0, y0, x1, y1);
    points = [[0, 0]]
    dist0 = dist([0, 0], i[0])
    dist1 = dist([0, 0], i[1])
    if (dist0<dist1):
        points = get_points_outside(points, 5, 5, 3, i[0][0], i[0][1], i[1][0], i[1][1]);
    else:
        points = get_points_outside(points, 5, 5, 3, i[1][0], i[1][1], i[0][0], i[0][1]);
    points.append([10, 10])
    return points

points = get_route(5, 5, 3, 0, 0, 10, 10);
x, y = zip(*points)
print("Points: ", points)
plt.scatter(x, y)
plt.savefig('foo.png')

# print(i.geoms[0].coords[0])
# print(i.geoms[1].coords[0])
