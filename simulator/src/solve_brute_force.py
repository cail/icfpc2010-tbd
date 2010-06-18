from itertools import *

def solve_brute_force(car, limit=3):
    fuels = product(*[range(1,limit)]*car.num_tanks)
    fuels = sorted(fuels, key=sum)
    
    for fuel in fuels:
        if car.test_on_fuel(fuel):
            return fuel
    
