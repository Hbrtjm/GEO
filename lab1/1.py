from random import uniforom,choice
from matplotlib.pyplot import plot 
from time import time

def det1(a,b,c):
    return (b[0]*c[1]-c[0]*b[1])-(a[0]*c[1]-a[1]*c[0])+(a[0]*b[1]-b[0]*a[1])

def det2(a,b,c):
    return ((a[0]-c[0])*(b[1]-c[1]))-((b[0]-c[0])*(a[1]-c[1]))

points = [ (random()*randint(-1000,1000),random()*randint(-1000,1000)) for _ in range(10**5) ]

start = time()
for i in range()det()


def calculate(generator,n,generator_name = "None",a=(-1.0,0.0),b=(1.0,1.0)):
    points = generator()
    for i in range(n):
        
def time_it(genertor_list)
    for generator_function,generator_name in generator_list:
        start = time()
        results = calculate(points)
        visualize(results)
        end = time()
        print (f"For {generator_name} elapsed time {end-start}")

def First_generator():
    return [ (uniform(-10**3,10**3),uniform(-10**3,10**3) for _ in range(10**5) ]

def Second_generator():
    return [ (uniform(-10**14,10**14,uniform(-10**14,10**14) for _ in range(10**5)  ]

def Third_generator():
    result = []
    for _ in range(10**3):
        x = uniform(-100,100)
        result.append((x,uniform(-sqrt(100**2 - x**2),sqrt(100*2 - x**2)))
    return result

def Foruth_generator():
    

functions = [(First_generator,"10 ^ 5 from (-1000,1000)"), (Second_generator,"10 ^ 5 from (-10^14,10^14)"),(Third_generator,"Numbers that are constrained to a circle of radious 100 and center (0,0)"),(Fourth_generator,)]


time_it()


