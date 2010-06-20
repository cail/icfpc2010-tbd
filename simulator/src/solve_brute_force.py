from math import *
from itertools import *

from car import fuel_to_stream

def solve_brute_force(car):
    n = 20000
    limit = int(0.5 + exp(log(n)/car.num_tanks))
    
    fuels = product(*[range(1,limit)]*car.num_tanks)
    fuels = sorted(fuels, key=lambda fuel: len(fuel_to_stream(list(fuel))))
    
    for fuel in fuels:
        if car.test_on_fuel(fuel):
            return list(fuel)
    
