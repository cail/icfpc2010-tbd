from time import clock
from math import *
from itertools import *

from car import fuel_to_stream, numpy_fuel

print 'prepairing fuels for brute force...',
fuels_to_search = {}
for i in range(1, 7):
    n = 40000
    limit = int(0.5 + exp(log(n)/i))
    
    fuels = list(product(*[range(1,limit)]*i))
    fuel_lens = dict((fuel,len(fuel_to_stream(list(fuel)))) for fuel in fuels)

    fuels = sorted(fuels, key = fuel_lens.get)
    #print [(f, fuel_lens[f]) for f in fuels[:10]]
    fuels_to_search[i] = map(numpy_fuel, fuels)
print 'done'     

def solve_brute_force(car):
    timeout = 0.5
    start = clock()
    
    for fuel in fuels_to_search[car.num_tanks]:
        if clock()-start > timeout:
            break
        if car.test_on_fuel(fuel):
            return list(fuel)
    
