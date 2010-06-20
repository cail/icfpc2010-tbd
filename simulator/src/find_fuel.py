from pprint import pprint, pformat
from car import fuel_to_stream
from solve_brute_force import solve_brute_force
from solve_lp import solve_LP
from solve_mc import solve_monte_carlo

from functools import partial

USE_CACHE = False
# set it to false if you improve solver and want to calculate better solutions


solve_monte_carlo_size2 = partial(solve_monte_carlo, size=2) 
solve_monte_carlo_size3 = partial(solve_monte_carlo, size=3) 

def find_fuel(car):
    best = None
    best_len = 1e100
    
    for f in [solve_brute_force, 
              solve_monte_carlo_size2, 
              solve_monte_carlo_size3,
              solve_LP]:
        print f,
        fuel = f(car)
        if fuel is not None:
            assert car.test_on_fuel(fuel), fuel
            l = len(fuel_to_stream(fuel))
            print 'solved', l
            if l < best_len:
                best_len = l
                best = fuel
        else:
            print
            
    return best

CACHE_FILE = 'car_fuel_cache.txt'

def load_cache():
    global cache
    with open(CACHE_FILE) as cache_file:
        cache = eval(cache_file.read())
        
def save_cache():
    global cache
    with open(CACHE_FILE,'wt') as cache_file: 
        print>>cache_file, "# car stream: fuel stream"
        dump = pformat(cache).replace("{", "{\n").replace("}", "\n}")
        print >> cache_file, dump



def find_fuel_stream(car):
    if USE_CACHE:
        load_cache()
        if car.representation in cache:
            return cache[car.representation]
    
    fuel = find_fuel(car)
    if fuel == None:
        return
        
    print(fuel) 
    suffix = fuel_to_stream(fuel)
    
    load_cache()
    cached = cache.get(car.representation)
    if cached is None or len(cached) > len(car.representation):
        cache[car.representation] = suffix
        save_cache()
    else:
        return cached
        
    return suffix
