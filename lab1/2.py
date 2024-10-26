from random import uniform
from matplotlib import pyplot as plt
from time import time
import numpy as np

def First_generator(n):
    return [(uniform(-10**3, 10**3), uniform(-10**3, 10**3)) for _ in range(n)]

def Second_generator(n):
    return [(uniform(-10**14, 10**14), uniform(-10**14, 10**14)) for _ in range(n)]

def Third_generator(n):
    result = []
    for _ in range(n):
        theta = uniform(0, 2 * np.pi)
        R = 100
        result.append((R * np.cos(theta), R * np.sin(theta)))
    return result

def Fourth_generator(n):
    return [(x, 0.05 * x + 0.05) for x in (uniform(-1000, 1000) for _ in range(n))]

def det2x2(a, b, c):
    return (a[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - c[1])

def det3x3(a, b, c):
    return np.linalg.det([[a[0], a[1], 1], [b[0], b[1], 1], [c[0], c[1], 1]])

def det_np_2x2(a, b, c):
    return np.linalg.det([[a[0] - c[0], a[1] - c[1]], [b[0] - c[0], b[1] - c[1]]])

def det_np_3x3(a, b, c):
    return np.linalg.det([[a[0], a[1], 1], [b[0], b[1], 1], [c[0], c[1], 1]])

def orientation(a, b, c, epsilon, detFun):
    det = detFun(a, b, c)
    if abs(det) < epsilon:
        return 0  # Collinear
    elif det > epsilon:
        return 1  # Above the line
    else:
        return 2  # Below the line

SIZES = [1,0.1,0.01]

def decode_colors(orient):
    cols = [ (0,0,1), (0,1,0) , (1,0,0) ]
    res = []
    for i in range(len(orient)):
        res.append(cols[orient[i]])
    return res

def calculate(points=[],n=100,epsilon=0,a=(-1.0,0.0),b=(1.0,0.1),detFun=det3x3,dot_size=1,generator_name="generated.tex",det_name=""):
    states = [0,0,0]
    orient = [ None for _ in range(n) ]
    for i in range(n):
        orient[i] = orientation(points[i],a,b,epsilon,detFun)
        states[orient[i]] += 1
    z = zip(*points)
    decoded = decode_colors(orient)
    plt.scatter(*z,c=decoded,s=[SIZES[dot_size] for _ in range(n)])
    plt.axline(a, b, markersize=2)
    plt.savefig(f"{generator_name}_{det_name}_marked.png")
    return states

def time_it(generator_list, epsilons, dets):
    for generator_function, n, generator_name, size in generator_list:
        tex_filename = f"{generator_name}.tex"
        with open(tex_filename, "w") as f:
            f.write("\\begin{table}[ht]\n")
            f.write("    \\centering\n")
            f.write(f"    \\caption{{Tabela różnic czasów obliczeń i tolerancji dla generatora {generator_name.replace("_"," ")}}}\n")
            f.write("    \\begin{tabular}{@{}llccccc@{}}\n")
            f.write("        \\toprule\n")
            f.write("        Tolerancja \\epsilon & Nazwa wyznacznika & Czas obliczeń (s) & Punkty powyżej prostej & Punkty poniżej prostej & Punkty na prostej \\\\ \\midrule\n")
        points = generator_function(n)
        plt.scatter(*zip(*points),s=[SIZES[size] for _ in range(n)])
        plt.savefig(generator_name + ".png")
        for epsilon in epsilons:
            with open(tex_filename, "a") as f:
                f.write(f"        \\multicolumn{{6}}{{c}}{{Epsilon = {epsilon}}} \\\\ \\midrule\n")
            for detFun, detName in dets:
                start = time()
                states = calculate(points=points, n=n, epsilon=epsilon, a=(-1.0, 0.0), b=(1.0, 0.1), detFun=detFun, dot_size=size, generator_name=generator_name,det_name=detName)
                end = time()
                with open(tex_filename, "a") as f:
                    f.write(f"        {epsilon} & {detName} & {end - start:.2f} & {states[1]} & {states[2]} & {states[0]} \\\\\n")
        with open(tex_filename, "a") as f:
            f.write("        \\bottomrule\n")
            f.write("    \\end{tabular}\n")
            f.write("\\end{table}\n")

epsilons = [0, 10**-14, 10**-12, 10**-10, 10**-8]
dets = [(det3x3, "Własny wyznacznik 3x3"), (det2x2, "Własny wyznacznik 2x2"), (det_np_2x2, "Wyznacznik numpy 2x2"), (det_np_3x3, "Wyznacznik numpy 2x2")]

functions = [
    (First_generator, 10**5, "10^5_z_przedziału_(-1000,1000)", 2),
    (Second_generator, 10**5, "10^5_z_przedziału_(-10^14,10^14)", 2),
    (Third_generator, 10**3, "koła_o_promieniu_100", 1),
    (Fourth_generator, 10**3, "Lini_a_b_y=0.05x+0.05", 0)
]

time_it(functions, epsilons, dets)
