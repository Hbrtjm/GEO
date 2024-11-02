
from random import uniform, randint
import matplotlib.pyplot as plt
import numpy as np
from time import time
import math
import copy


def det(a,b,c):
    return (b[0]*c[1]-c[0]*b[1])-(a[0]*c[1]-a[1]*c[0])+(a[0]*b[1]-b[0]*a[1])

def First_generator(n=100):
    return [ (uniform(-100,100),uniform(-100,100)) for _ in range(n) ]

# ================================= Graham =================================

def merge(L, R):
    new = []
    i = j = 0
    while i < len(L) and j < len(R):
        if det((0,0),L[i],R[j]) < 0:
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

def point_generator(n=20,x_max=100,x_min=-100,y_max=100,y_min=-100):
    return [ (uniform(x_min,x_max),uniform(y_min,y_max)) for _ in range(n) ] 

def det2x2(a,b,c):
    return ((a[0]-c[0])*(b[1]-c[1]))-((b[0]-c[0])*(a[1]-c[1]))

def Graham(points,detFun=det2x2):
    result = []
    points = sorted(points, key=lambda p: (p[1], p[0])) 
    starting_point = points[0]
    sorted_points = sorted(points[1:], key=lambda p: math.atan2(p[1] - starting_point[1], p[0] - starting_point[0]))
    fig, ax = plt.subplots()
    
    ax.set_aspect('equal','box')
    # ax.set_xlim(x_min,x_max)
    # ax.set_ylim(y_min_y_max)
    for point in points:
        ax.plot(*point, 'bo')
    
    print("Sorting points")
    points = radial_sort(points)
    print(points)
    # Start building the convex hull
    result = [starting_point, sorted_points[0]]
    ax.plot(*starting_point,'ro')
    ax.plot(*sorted_points[0],'ro')   
    first_line, = ax.plot([starting_point[0], sorted_points[0][0]],[starting_point[1],sorted_points[0][1]],'b-')
    lines_stack = [first_line]
    print("Creating hull")
    start = time()
    previous_point = starting_point 
    for i, point in enumerate(sorted_points[1:]):
        ax.plot(*point, 'ro')
        plt.draw()
        plt.pause(0.2)
        while len(result) > 1 and detFun(result[-2], result[-1], point) < 0:
            lines_stack[-1].remove()
            lines_stack.pop()
            result.pop()
        line, = ax.plot([point[0], result[-1][0]], [point[1], result[-1][1]],'b-')
        lines_stack.append(line)
        result.append(point)

    finish = time()

    
    print(f"Finished after {finish - start} seconds")
    print(result)
    return result

def print_hull(points,hull):
    plt.scatter(*zip(*points))
    n = len(hull)
    for i in range(n):
        print(f"From: {hull[i]} to {hull[(i+1)%n]}")
        x_values = [hull[i][0], hull[(i+1) % n][0]]
        y_values = [hull[i][1], hull[(i+1) % n][1]]
        
        # Plot a line between the current point and the next
        plt.plot(x_values, y_values, 'r-')
    plt.show()

# ================================= Jarvis ================================= 


def squared_distance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

E = 1e-5


def follows(prev, current, next):
    d = det(prev, current, next)
    if d < -E:
        return True  
    if d > E:
        return False
    return squared_distance(prev, current) < squared_distance(prev, next)

def choose_next(points, last, current, fig, ax):
    act = current
    for point in points:
        if act == last or follows(last, act, point):
            if act != current:
                ax.plot(*act, 'bo') 
            act = point
            ax.plot(*point, 'ro')
    return act

def Jarvis(points):
    points_set = copy.deepcopy(points)
    fig, ax = plt.subplots()
    ax.set_aspect('equal','box')
    for point in points:
        ax.plot(*point, 'bo')
    start = min(points_set, key=lambda x: (x[1], x[0]))  
    hull = [start]
    
    current_point = start
    
    while True:
        next_point = choose_next(points_set, hull[-1], current_point, fig, ax)
        ax.plot(*point, 'go')
        if next_point == start:
            break
        line, = ax.plot([point[0], hull[-1][0]], [point[1], hull[-1][1]],'b-')
        hull.append(next_point)
        current_point = next_point
    
    return hull


# =================================  Tests =================================

points1 = First_generator()
plt.figure(figsize=(4,4))
plt.scatter(*zip(*points1))
plt.show()

points_set = [points1] #,points2,points3,points4]

for points in points_set:
    print_hull(points,Jarvis(points))

