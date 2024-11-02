import matplotlib.pyplot as plt
from random import uniform
import math
from time import time


def det3x3(a, b, c):
    return (
        (b[0] * c[1] - c[0] * b[1])
        - (a[0] * c[1] - a[1] * c[0])
        + (a[0] * b[1] - b[0] * a[1])
    )


def First_generator(n=100):
    return [(uniform(-100, 100), uniform(-100, 100)) for _ in range(n)]


def merge(L, R):
    new = []
    i = j = 0
    while i < len(L) and j < len(R):
        if det3x3((0, 0), L[i], R[j]) < 0:
            new.append(L[i])
            i += 1
        else:
            new.append(R[j])
            j += 1
    new.extend(L[i:])
    new.extend(R[j:])
    return new


def radial_sort(points):
    if len(points) < 2:
        return points
    mid = len(points) // 2
    left = radial_sort(points[:mid])
    right = radial_sort(points[mid:])
    return merge(left, right)


def point_generator(n=20, x_max=100, x_min=-100, y_max=100, y_min=-100):
    return [(uniform(x_min, x_max), uniform(y_min, y_max)) for _ in range(n)]


def det2x2(a, b, c):
    return ((a[0] - c[0]) * (b[1] - c[1])) - ((b[0] - c[0]) * (a[1] - c[1]))


def convex_hull(points, detFun=det2x2):
    result = []
    points = sorted(points, key=lambda p: (p[1], p[0]))
    starting_point = points[0]
    sorted_points = sorted(
        points[1:],
        key=lambda p: math.atan2(p[1] - starting_point[1], p[0] - starting_point[0]),
    )

    print("Sorting points")
    points = radial_sort(points)
    print(points)
    # Start building the convex hull
    result = [starting_point, sorted_points[0]]
    print("Creating hull")
    start = time()
    for point in sorted_points[1:]:
        while len(result) > 1 and detFun(result[-2], result[-1], point) < 0:
            result.pop()
        result.append(point)
    finish = time()

    print(f"Finished after {finish - start} seconds")
    print(result)
    return result


def print_hull(points, hull):
    plt.scatter(*zip(*points))
    n = len(hull)
    for i in range(n):
        print(f"From: {hull[i]} to {hull[(i+1)%n]}")
        x_values = [hull[i][0], hull[(i + 1) % n][0]]
        y_values = [hull[i][1], hull[(i + 1) % n][1]]

        # Plot a line between the current point and the next
        plt.plot(x_values, y_values, "r-")
    plt.show()


points = point_generator(n=100)
print_hull(points, convex_hull(points))
