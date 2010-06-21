from time import clock
from random import randrange
from numpy import *

from copy import deepcopy

from car import fuel_to_stream

def solve_monte_carlo(car, size=2, timeout=1.0):
    best = None
    best_len = 1e100
    
    fuel = [zeros((size,size), dtype=object) for i in range(car.num_tanks)]

    start = clock()
    
    for attempt in xrange(10000000):
        if clock()-start > timeout:
            break
        for i in range(car.num_tanks):
            for j in range(size):
                for k in range(size):
                    fuel[i][j,k] = randrange(3)
            fuel[i][0,0] += 1
        if car.test_on_fuel(fuel):
            l = len(fuel_to_stream(fuel))
            if l < best_len:
                best_len = l
                best = deepcopy(fuel)
                 
    return best