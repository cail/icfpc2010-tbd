from pprint import pprint
import csv


from car import Car, fuel_to_stream
from solve_brute_force import solve_brute_force
from solve_lp import solve_LP
from scheme_as_sat import generate_scheme_for_fuel



def find_fuel(car):
    for f in [solve_brute_force, solve_LP]:
#    for f in [solve_brute_force]:
        fuel = f(car)
        if fuel is not None:
            print 'solved with', f
            return fuel


def solve(car_string):
    car = Car.from_stream(car_string.strip())
    print car
    
    fuel = find_fuel(car)
    
    if fuel is None:
        print 'fail'
        return
    
    pprint(fuel) 
    assert car.test_on_fuel(fuel)
    
    suffix = fuel_to_stream(fuel)
    print len(suffix), suffix
    
    suffix = map(int, suffix)

    scheme = generate_scheme_for_fuel(suffix)
    
    if scheme is None:
        return None
    
    s = str(scheme)
    print len(s.split('\n'))-2,'gates'
    return s


if __name__ == '__main__':
    
    data = csv.reader(open('../data/car_data_sorted'))
    
    total = 0
    solved = 0
    
    for line in data:
        if line == []:
            continue
        
        car_no, stream = line
        
        if car_no == '219':
            continue

        total += 1
        
        print car_no
        result = solve(stream)
        if result is not None:
            solved += 1
            
        print 'solved ', solved, '/', total
            
    print 'solved ', solved, '/', total
    #s = solve('12222000000000010')
    #print s
    
    
    
    #print scheme
    
    pass