try:
    import psyco
    psyco.full()
except ImportError:
    print "you do not have psyco, but (hopefully) it's fine"

from pprint import pprint
import csv
import re
from random import shuffle, random, seed
#seed(123)

import sys
from multiprocessing import Pool, TimeoutError


from car import Car, fuel_to_stream
from scheme_as_sat import generate_scheme_for_fuel
from submit_fuel import submit_fuel, login, submit_test_car_fuel
from factory_builder import fast_generate_scheme_for_fuel
from scheme import key
    
    
VERBOSE = True

max_suffix = 15

def solve(car_string):
    assert car_string.strip() != '0'
    
    car = Car.from_stream(car_string.strip())
    if VERBOSE:
        print car
    
    suffix = find_fuel_stream(car)
    
    
    if suffix is None:
        print 'fail'
        return
    
    if len(suffix) > 2000:
        print 'too long'
        return
    
    print len(suffix), suffix
    
    suffix = map(int, suffix)
    if len(suffix) < max_suffix:
        scheme = generate_scheme_for_fuel(suffix)
    else:
        scheme = fast_generate_scheme_for_fuel(suffix)
        
    if scheme is None:
        return None
    s = str(scheme)
    
    print len(s.split('\n')) - 2, 'gates'
    return s


if __name__ == '__main__':
    
    print """
    Usage options:
      skipsubmitted     | skip already submitted cars
      startwith <carno> | start from specified <carno>, discard all cars before
      endwith <carno>   | end with specified <carno>, discard all cars after
      maxsuffix <no>    | max fuel suffix to run with vlad's analysis
      minsuppliers <no> | minimum number of suppliers, discard all less
      maxsuppliers <no> | max number of suppliers, discard all above
      sortbycarsize     | sort by car size, else uses random
      TESTONLY          | submit agaits TEST server. results are writted into test_data
      SHOWONLY          | only shows the list of cars to run with, no run
    """
    
    data = csv.reader(open('../data/car_ids'))
    data = list(data)
    
    suppliers = {}
    for line in data:
        if len(line) == 0:
            continue
        id, sup = line
        suppliers[int(id)] = int(sup)

    skipsubmitted = True
    start_with = None
    end_with = None
    minsuppliers = maxsuppliers = 12
    
    sortbycarsize = False
    testonly = False
    showonly = False
    for i, v in enumerate(sys.argv):
        if v == 'skipsubmitted':
            skipsubmitted = True
        if v == 'startwith':
            start_with = int(sys.argv[i + 1])
        if v == 'endwith':
            end_with = int(sys.argv[i + 1])
        if v == 'maxsuffix':
            max_suffix = int(sys.argv[i + 1])
        if v == 'minsuppliers':
            minsuppliers = int(sys.argv[i + 1])
        if v == 'maxsuppliers':
            maxsuppliers = int(sys.argv[i + 1])
        if v == 'sortbycarsize':
            sortbycarsize = True
        if v == 'TESTONLY':
            testonly = True
        if v == 'SHOWONLY':
            showonly = True
            

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
        if len(line) < 2:
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
        
        tasks.append((car_no, suppliers[car_no], stream))
    
    
    if sortbycarsize:
        tasks.sort(key=lambda (n, sup, s): (sup, len(s)))
    else:
        tasks.sort(key=lambda (n, sup, s): (sup, random()*0.01))
    
    if start_with or end_with:
        start_idx = 0
        end_idx = len(tasks)
        for i, id in enumerate(tasks):
            if id[0] == start_with:
                start_idx = i
            if id[0] == end_with:
                end_idx = i+1
        tasks = tasks[start_idx:end_idx] 
        print "start from {0}'th element, end with {1}'th element".format(start_idx, end_idx)


    total = 0
    solved = 0
    
    browser = None
    
    # this is to prevent big delay on startup
    if not showonly:
        from find_fuel import find_fuel_stream
        
    
    for car_no, sup, stream in tasks:
        
        #if sup == 1:
        #    continue
        
        print "CAR #", car_no, '\t\t', sup, 'suppliers', "\t\t", len(stream), "\tlength"  
        
        total += 1
        
        if showonly:
            
            continue

        result = solve(stream)
        if result is not None:
            print 'submitting: '
            
            # store it temporary for debuggin
            open('temp_solution', 'w').write(result)

                
            if testonly:
                tres = submit_test_car_fuel(stream, result)
                print tres
                if tres.find('Good!') != -1:
                    fout = open('test_data', 'a')
                    fout.write(repr((car_no, result)))
                    fout.close()
            else:
                if browser is None:
                    # disabled because there is a risk of timeout
                    print 'login',
                    browser = login()
                    print 'ok'
                print submit_fuel(car_no, result, br=browser)
            
            solved += 1
            
        print 'solved ', solved, '/ current ', total, '/ total ', len(tasks)
        
        
            
    print 'finally solved ', solved, '/', total
   
    
