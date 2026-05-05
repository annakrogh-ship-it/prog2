""" MA3.py

Student: Anna Krogh
Mail: anna.krogh04@gmail.com
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import numpy as np
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    cirkel = []
    square = []
    for i in range(n+1):
        x = random.uniform(-1, 1) 
        y = random.uniform(-1, 1)
        if ((x**2) + (y**2)) <= 1:
            cirkel.append([x, y])
        else:
            square.append([x, y])
    plt.plot([n[0] for n in cirkel], [n[1] for n in cirkel], '.', color='red')
    plt.plot([n[0] for n in square], [n[1] for n in square], '.', color='blue')
    plt.show()
    return 4 * (len(cirkel)/ (len(cirkel) + len(square)))


def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    #d is the number of dimensions of the sphere 
    p = [[random.uniform(-1, 1) for num in range(d)] for numb in range(n)]
    inside = list(filter(lambda x: np.sum([n ** 2 for n in x]) <= 1 , p))   
    return (2 ** d) * len(inside) / len(p)
    

def hypersphere_exact(n,d): #Ex2, real value
    #n is the number of points
    # d is the number of dimensions of the sphere 
    return (np.pi ** (d/2)) / m.gamma((d/2) + 1)
    

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex:
        results = ex.map(sphere_volume, [n for i in range(np)], [d for i in range(np)])
    average = sum([r for r in results]) / np  
    return average

def points(n, d):
    p = [[random.uniform(-1, 1) for num in range(d)] for numb in range(n)]
    return p
#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex:
        result = ex.map(points, [n // np for i in range(np)], [d for i in range(np)])
        p = []
        for r in result:
            p += r
        inside = list(filter(lambda x: sum([n ** 2 for n in x]) <= 1 , p))
    return (2 ** d) * len(inside) / len(p)

   
def main():
    
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    average = sum([sphere_volume(n,d) for y in range(10)]) / 10
    stop = pc()
    print(f'average is {average}')
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    start = pc()
    average = sphere_volume_parallel1(n,d)
    stop = pc()
    print(f'average is {average}')
    print(f"Parallel time is {stop-start}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    value = sphere_volume(n,d)
    stop = pc()
    print(value)
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    start = pc()
    value = sphere_volume_parallel2(n,d)
    stop = pc()
    print(value)
    print(f"Parallel time is {stop-start}")

    
    

if __name__ == '__main__':
	main()

