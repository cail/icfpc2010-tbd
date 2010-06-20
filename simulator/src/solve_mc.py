from random import randrange
from numpy import *

from car import fuel_to_stream

def solve_monte_carlo(car, size=2, attempts=1000):
    best = None
    best_len = 1e100
    
    fuel = [zeros((size,size)) for i in range(car.num_tanks)]
    
    for attempt in xrange(attempts):
        for i in range(car.num_tanks):
            for j in range(size):
                for k in range(size):
                    fuel[i][j,k] = randrange(10)
            fuel[i][0,0] += 1
        if car.test_on_fuel(fuel, num_tests=500):
            l = len(fuel_to_stream(fuel))
            if l < best_len:
                best_len = l
                best = fuel
                
    return best