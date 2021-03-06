from pprint import pprint, pformat
from car import fuel_to_stream
from solve_brute_force import solve_brute_force
from solve_lp import solve_LP
from solve_mc import solve_monte_carlo
from collections import defaultdict
from pprint import pprint

from functools import partial

USE_CACHE = True
# set it to false if you improve solver and want to calculate better solutions


def solve_monte_carlo_size2(car):
    return solve_monte_carlo(car, size=2) 

def solve_monte_carlo_size3(car):
    return solve_monte_carlo(car, size=3) 

def solve_monte_carlo_size6(car):
    return solve_monte_carlo(car, size=6) 


who_solved = defaultdict(int)

def find_fuel(car):
    best = None
    best_len = 1e100
    best_solver = 'nobody'
    
    for f in [solve_brute_force, 
              solve_monte_carlo_size2,
              #solve_monte_carlo_size3,
              #solve_monte_carlo_size6,
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
                best_solver = f
            if f == solve_brute_force: # brute force always finds best solution
                break
        else:
            print
    
    who_solved[best_solver] += 1
    print 'solvers stats:'
    pprint(dict(who_solved))      
      
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
