from pprint import pprint
import csv
from random import shuffle, random
import sys
from multiprocessing import Pool, TimeoutError


from car import Car, fuel_to_stream
from scheme_as_sat import generate_scheme_for_fuel
from find_fuel import find_fuel_stream
from submit_fuel import submit_fuel, login
    
    
VERBOSE = True

def solve(car_string):
    assert car_string.strip() != '0'
    
    car = Car.from_stream(car_string.strip())
    if VERBOSE:
        print car
    
    suffix = find_fuel_stream(car)
    
    if suffix is None:
        print 'fail'
        return
    
    print len(suffix), suffix
    
    if len(suffix) > 40:
        print 'skip'
        return
    
    suffix = map(int, suffix)

    scheme = generate_scheme_for_fuel(suffix)
    
    if scheme is None:
        return None
    
    s = str(scheme)
    print len(s.split('\n'))-2,'gates'
    return s


if __name__ == '__main__':
    
    data = csv.reader(open('../data/car_ids'))
    data = list(data)
    
    suppliers = {}
    for line in data:
        if len(line) == 0:
            continue
        id, sup = line
        suppliers[int(id)] = int(sup)
        
    
    data = csv.reader(open('../data/car_data'))
    data = list(data)
    
    tasks = []
    
    for line in data:
        if line == []:
            continue
        car_no, stream = line
        car_no = int(car_no)
        stream = stream.strip()
        
        if car_no == 219:
            continue
        
        tasks.append((car_no,suppliers[car_no],stream))

    tasks.sort(key = lambda (n, sup, s): (sup, random()*0.01))
    
    total = 0
    solved = 0
    
    browser = None
    
    for car_no, sup, stream in tasks:
        
        if sup == 1:
            continue
        
        print "CAR #", car_no, '   ', sup, 'suppliers'
        total += 1
        result = solve(stream)
        if result is not None:
            if browser is None:
                print 'login',
                browser = login()
                print 'ok'
                
            print 'submitting...'
            print submit_fuel(car_no, result, br=browser)
            
            solved += 1
            
        print 'solved ', solved, '/', total
        
        
            
    print 'finally solved ', solved, '/', total
   
    
