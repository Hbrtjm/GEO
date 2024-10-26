from random import uniform,choice
from matplotlib import pyplot as plt
from time import time
import numpy as np

def decode_colors(orient):
    cols = [ (0,0,1), (0,1,0) , (1,0,0) ]
    res = []
    for i in range(len(orient)):
        res.append(cols[orient[i]])
    return res

def det3x3(a,b,c):
    return (b[0]*c[1]-c[0]*b[1])-(a[0]*c[1]-a[1]*c[0])+(a[0]*b[1]-b[0]*a[1])

def det2x2(a,b,c):
    return ((a[0]-c[0])*(b[1]-c[1]))-((b[0]-c[0])*(a[1]-c[1]))

def make_matrix_3x3(a,b,c):
    return np.matrix([[a[0],a[1],1],[b[0],b[1],1],[c[0],c[1],1]])

def make_matrix_2x2(a,b,c):
    return np.matrix([[a[0]-c[0],a[1]-c[1]],[b[0]-c[0],b[1]-c[1]]])

def det_np_3x3(a,b,c):
    return np.linalg.det(make_matrix_3x3(a,b,c))

def det_np_2x2(a,b,c):
    return np.linalg.det(make_matrix_2x2(a,b,c))

def calculate(generator,n=100,epsilon=0,a=(-1.0,0.0),b=(1.0,1.0),detFun=det1):
    states = [0,0,0]
    points = generator(n)
    orient = [ None for _ in range(n) ]
    for i in range(n):
        orient[i] = orientation(points[i],a,b,epsilon,detFun)
        states[orient[i]] += 1
    z = zip(*points)
    #decoded = decode_colors(orient)
    #plt.scatter(*z,c=decoded)
    #plt.show()
    return states
def orientation(a,b,c,epsilon,detFun):
    det = detFun(a,b,c)
    if det < epsilon and det > -epsilon:
        return 0 # Colinear
    elif det > epsilon:
        return 1 # Positive orientation to the line
    else:
        return 2 # Negative orientation to the line

def time_it(generator_list,epsilons,dets):
    for generator_function,n,generator_name in generator_list:
        with open(f"{generator_name}.txt","w") as f:
            f.write("epsilon,det,time,s1,s2,s3\n")
        for epsilon in epsilons:
            for detFun,detName in dets:
                #epsilon = 10
                #detFun = det2
                start = time()
                states = calculate(generator_function,n=n,epsilon=epsilon,detFun=detFun)
                end = time()
                print (f"For {generator_name} elapsed time {end-start} for epsilon {epsilon}\nAbove: {states[1]} Below: {states[2]} Co-linear: {states[0]} ")
                with open(f"{generator_name}.txt","a") as f:
                    f.write(f"{epsilon},{detName},{end-start},{states[1]},{states[2]},{states[0]}\n")
def First_generator(n):
    return [ (uniform(-10**3,10**3),uniform(-10**3,10**3)) for _ in range(n) ]

def Second_generator(n):
    return [ (uniform(-10**14,10**14),uniform(-10**14,10**14)) for _ in range(n)  ]

def Third_generator(n):
    result = [ ]
    for _ in range(n):
        # x = uniform(-100,100)
        # result.append((x,uniform(-sqrt(100**2 - x**2),sqrt(100*2 - x**2)))
        theta = uniform(0,2*np.pi)
        R = 100
        result.append((R*np.cos(theta),R*np.sin(theta)))
    return result

def Fourth_generator(n):
    result = []
    for _ in range(n):
        #t = uniform(-500,500)
        #result.append((t*2,t*0.1))
        x = uniform(-1000,1000)
        result.append((x,0.05*x+0.05))
    return result

    
epsilons = [0,10**-14,10**-12,10**-10,10**-8]

dets = [(det1,"First own"),(det2,"Second own"),(det_np_2x2,"First np"),(det_np_3x3,"Second np")]

functions = [(First_generator,10**5,"10^5_from_(-1000,1000)"), (Second_generator,10**5,"10^5_from_(-10^14,10^14)"),(Third_generator,10**5,"Circle_of_radious_100_and_center_(0,0)"),(Fourth_generator,10**5,"Line_x,y_=v*t,_v=0,0.1,_t_in_R")]

time_it(functions,epsilons,dets)
