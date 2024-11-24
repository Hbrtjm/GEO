limit = 4

def previous_p(index, n):
    return (index + n - 1) % n

def next_p(index, n):
    return (index + 1) % n

def is_y_monotonic(polygon):
    n = len(polygon)
    min_index = get_min_index(polygon)
    max_index = get_max_index(polygon)
    # Top to bottom
    i = max_index
    while min_index != i:
        j = next_p(i,n)
        if polygon[i][1] < polygon[j][1]:
            return False
        i = next_p(i,n)
    # Bottom to top - left
    i = min_index
    while max_index != i:
        j = next_p(i,n)
        if polygon[i][1] > polygon[j][1]:
            return False
        i = next_p(i,n)
    return True

def det(a,b,c):
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])

def get_max_index(points):
    return max(range(len(points)), key=lambda i: (points[i][1], -points[i][0]))

def get_min_index(points):
    return min(range(len(points)), key=lambda i: (points[i][1], points[i][0]))

def divide(polygon):
    n = len(polygon)
    left_right = [0] * n
    min_index = get_min_index(polygon)
    max_index = get_max_index(polygon)
    left_right[max_index] = 0
    left_right[min_index] = 1 # Some problem may arise here, but it passes the tests
    i = max_index
    while i != min_index:
        left_right[i] = 0
        i = next_p(i, n)
    i = min_index
    while i != max_index:
        left_right[i] = 1 
        i = next_p(i, n)
    return left_right

def check_if_inside(a, b, c, c_side, epsilon=1e-18):
    d = det(a, b, c)
    if  c_side == 0:
        return d < epsilon
    return d > epsilon


def build_events(polygon):
    n = len(polygon)
    starter = get_max_index(polygon)
    end = get_min_index(polygon)
    left = previous_p(starter, n)
    right = next_p(starter, n)
    result = [starter]

    while left != end or right != end:
        if polygon[left][1] > polygon[right][1]:
            result.append(left)
            left = previous_p(left, n)
        elif polygon[left][1] < polygon[right][1]:
            result.append(right)
            right = next_p(right, n)
        else:
            if polygon[left][0] < polygon[right][0]:
                result.append(left)
                left = previous_p(left, n)
            else:
                result.append(right)
                right = next_p(right, n)

    result.append(end)
    return starter, result[1], result[2:]

# Unused
def draw_polygon_other(triangles, polygon, save_steps, step):
    """Visualize the current state of the triangulation."""
    fig, ax = plt.subplots()
    x, y = zip(*polygon)
    ax.plot(x + (x[0],), y + (y[0],), 'k-', label="Polygon") 
    for triangle in triangles:
        x_tri = [polygon[triangle[0]][0], polygon[triangle[1]][0], polygon[triangle[2]][0]]
        y_tri = [polygon[triangle[0]][1], polygon[triangle[1]][1], polygon[triangle[2]][1]]
        ax.fill(x_tri + [x_tri[0]], y_tri + [y_tri[0]], alpha=0.3, color="blue")

    ax.scatter(x, y, color='red', zorder=5)
    

    ax.set_title(f"Triangulation Step {step}")
    plt.axis("equal")
    if save_steps:
        plt.savefig(f"step_{step}.png")

def triangulation(polygon):
    """
    Perform triangulation of a monotone polygon.
    :param polygon: List of vertices (x, y) in counter-clockwise order.
    :return: List of diagonals [(i, j), ...], where i, j are vertex indices.
    """
    print(len(polygon))
    if not is_y_monotonic(polygon):
        print("Not monotonic!")
        return []
    n = len(polygon)
    triangulation_result = []
    left_right = divide(polygon)  # Determine left/right chains
    start, second, events = build_events(polygon)  # Sorted vertices by y-coordinate
    stack = [start, second]

    for i, event in enumerate(events):
        # print(f"Stos:\n{stack}\Aktualny punkt:\n{event}\nPo stronie {'prawej' if left_right[event] == 0 else 'lewej'}")
        current_chain = left_right[event]
        if left_right[stack[-1]] != current_chain: # and left_right[stack[-1]] != -1:
            last = stack[-1]
            while len(stack) >= 1:
                top = stack.pop()
                if abs(event-top) > 1 and abs(event-top) != n-1:
                    triangulation_result.append([event, top])
                    # print(f"Dodano przekątną z pierwszego warunku {[event,top]}")
                    # draw_polygon_tri(polygon, [(polygon[x], polygon[y]) for (x, y) in triangulation_result])
            stack.append(last)
            stack.append(event)
        else:
            while len(stack) > 1 and check_if_inside(polygon[event], polygon[stack[-1]],polygon[stack[-2]],left_right[stack[-1]]):
                    # print(f"Sprawdzanie, czy punkt jest wewnątrz {event} -> {stack[-1]} -> {stack[-2]}")
                    if abs(event-stack[-2]) > 1 and abs(event-stack[-2]) != n-1:
                        triangulation_result.append([event,stack[-2]])
                        # print(f"Dodano przekątną z drugiego warunku {[event,stack[-2]]}")
                        # draw_polygon_tri(polygon, [(polygon[x], polygon[y]) for (x, y) in triangulation_result])
                    stack.pop()
            stack.append(event)

    # draw_polygon_tri(polygon, [(polygon[x], polygon[y]) for (x, y) in triangulation_result])
    return triangulation_result

# Testing
def convert_to_float32(table):
    """
    Converts a list of tuples containing float64 values to float32.
    :param table: List of tuples [(float64, float64), ...]
    :return: List of tuples [(float32, float32), ...]
    """
    return [(np.float32(x), np.float32(y)) for x, y in table]

import matplotlib.pyplot as plt
import numpy as np
# from scipy.spatial import ConvexHull

# Initialize global variables
polygon = []
fig, ax = plt.subplots()

def update_plot():
    global limit, polygon
    """Update the plot to display all current points and the result of the algorithm."""
    ax.clear()
    ax.set_title("Click to add points")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.axis("equal")
    x_range = (-1, 1)  # Set the range for the x-axis
    y_range = (-1, 1)  # Set the range for the y-axis
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    # Plot all points in the polygon
    if len(polygon) != 0:
        polygon = convert_to_float32(polygon)
        x_coords, y_coords = zip(*polygon)
        ax.scatter(x_coords, y_coords, color="blue", s=5, label="Points")

    # If there are more than 3 points, compute and display the convex hull
    n = len(polygon)
    
    if n >= limit:
        for i in range(n):
            ax.plot(
                [polygon[i][0], polygon[(i+1)%n][0]],
                [polygon[i][1], polygon[(i+1)%n][1]],
                'b-', label="Hull Edge" if "Hull Edge" not in ax.get_legend_handles_labels()[1] else "")
        trinagles = triangulation(polygon)
        for a, b in trinagles:
            ax.plot(
                [polygon[a][0], polygon[b][0]],
                [polygon[a][1], polygon[b][1]],
                'r-', label="Hull Edge" if "Hull Edge" not in ax.get_legend_handles_labels()[1] else "")
        print(polygon)
        print(trinagles)
    ax.legend()
    plt.draw()

def onclick(event):
    """Handle mouse click events to add points to the polygon."""
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        polygon.append((x, y))  # Append the clicked point to the polygon
        update_plot()

def main():
    """Main function to set up the interactive plot."""
    global limit
    limit_string = input("Ile minimalnie punktów wielokąta: ")
    if limit_string.isnumeric():
        limit = int(limit_string)
    fig.canvas.mpl_connect("button_press_event", onclick)
    update_plot()
    plt.show()

if __name__ == "__main__":
    main()
