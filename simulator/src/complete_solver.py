from pprint import pprint
import csv
import re
from random import shuffle, random, seed
#seed(123)

import sys
from multiprocessing import Pool, TimeoutError


from car import Car, fuel_to_stream
from scheme_as_sat import generate_scheme_for_fuel
from find_fuel import find_fuel_stream
from submit_fuel import submit_fuel, login, submit_test_car_fuel
from factory_builder import compile_factory
from scheme import key
    
    
VERBOSE = True

max_suffix = 30

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
    
    if len(suffix) < max_suffix:
        suffix = map(int, suffix)

        scheme = generate_scheme_for_fuel(suffix)
        if scheme is None:
            return None
        s = str(scheme)
    else:
        s = compile_factory(''.join(map(str,key))+suffix)
        
    print len(s.split('\n'))-2,'gates'
    return s


if __name__ == '__main__':
    
    print "Usage options: skipsubmitted | startwith <carno> | maxsuffix <no> | minsuppliers <no> | maxsuppliers <no> | sortbycarsize | TESTONLY"
    
    data = csv.reader(open('../data/car_ids'))
    data = list(data)
    
    suppliers = {}
    for line in data:
        if len(line) == 0:
            continue
        id, sup = line
        suppliers[int(id)] = int(sup)

    skipsubmitted = False
    start_with = None
    minsuppliers = 0
    maxsuppliers = 1000
    sortbycarsize = False
    testonly = False
    for i, v in enumerate(sys.argv):
        if v == 'skipsubmitted':
            skipsubmitted = True
        if v == 'startwith':
            start_with = int(sys.argv[i+1])
        if v == 'maxsuffix':
            max_suffix = int(sys.argv[i+1])
        if v == 'minsuppliers':
            minsuppliers = int(sys.argv[i+1])
        if v == 'maxsuppliers':
            maxsuppliers = int(sys.argv[i+1])
        if v == 'sortbycarsize':
            sortbycarsize = True
        if v == 'TESTONLY':
            testonly = True
            

    submittedcars = set()
    if skipsubmitted:
        submitted = open('../data/submitted_solutions.txt').readlines()
        for line in submitted:
            m = re.match(r"\s*(\d+)\:", line)
            if m:
                submittedcars.add(int(m.group(1)))
    
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
        
        # skip already submitted cars
        if car_no in submittedcars:
            continue
        
        if suppliers[car_no] < minsuppliers:
            continue
        if suppliers[car_no] > maxsuppliers:
            continue
        
        tasks.append((car_no,suppliers[car_no],stream))
    
    
    if sortbycarsize:
        tasks.sort(key = lambda (n, sup, s): (sup, len(s)))
    else:
        tasks.sort(key = lambda (n, sup, s): (sup, random()*0.01))
    
    if start_with:
        start_idx = 0
        for i, id in enumerate(tasks):
            if id[0] == start_with:
                start_idx = i
                break
        tasks = tasks[start_idx:] 
        print "skipping first {0} elements".format(start_idx)



    total = 0
    solved = 0
    
    browser = None
    
    for car_no, sup, stream in tasks:
        
        #if sup == 1:
        #    continue
        
        print "CAR #", car_no, '   ', sup, 'suppliers'
        total += 1
        result = solve(stream)
        if result is not None:
            print 'submitting: '
            
            # store it temporary for debuggin
            open('temp_solution', 'w').write(result)

                
            if testonly:
                tres = submit_test_car_fuel(stream, result)
                if tres.find('Good!') != -1:
                    fout = open('test_data', 'a')
                    fout.write(repr((car_no, result)))
                    fout.close()
            else:
                if False and browser is None:
                    # disabled because there is a risk of timeout
                    print 'login',
                    browser = login()
                    print 'ok'
                print submit_fuel(car_no, result, br=browser)
            
            solved += 1
            
        print 'solved ', solved, '/ current ', total, '/ total ', len(tasks)
        
        
            
    print 'finally solved ', solved, '/', total
   
    
