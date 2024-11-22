import matplotlib.pyplot as plt
from visualizer.main import Visualizer  # Assuming the Visualizer class is in a module named `visualizer`

visualizer = Visualizer()
visualizer.add_title("Interactive Point Adding")
visualizer.add_grid()
visualizer.axis_equal()

clicked_points = []

def onclick(event):
    """Handles mouse click events to add points to the visualizer."""
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        clicked_points.append((x, y))
        visualizer.add_point((x, y), color="red", s=5)
        visualizer.clear()
        for point in clicked_points:
            visualizer.add_point(point, color="blue", s=5)
        visualizer.show()

def main():
    """Main function to set up interactive plotting."""
    fig, ax = plt.subplots()
    ax.set_title("Click to add points")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    plt.axis("equal")
    fig.canvas.mpl_connect("button_press_event", onclick)
    plt.show()

if __name__ == "__main__":
    main()
