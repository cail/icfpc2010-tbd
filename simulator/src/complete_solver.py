from pprint import pprint
import csv
from random import shuffle
from multiprocessing import Pool, TimeoutError


from car import Car, fuel_to_stream
from scheme_as_sat import generate_scheme_for_fuel
from find_fuel import find_fuel_stream
from submit_fuel import submit_fuel, login
    

def solve(car_string):
    assert car_string.strip() != '0'
    
    car = Car.from_stream(car_string.strip())
    print car
    
    suffix = find_fuel_stream(car)
    
    if suffix is None:
        print 'fail'
        return
    
    print len(suffix), suffix
    
    if len(suffix) > 30:
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
    
    data = csv.reader(open('../data/car_data'))
    data = list(data)
    
    shuffle(data)
    
    total = 0
    solved = 0
    
    #pool = Pool()
    submit_tasks = []
    
    browser = None
    
    for line in data:
        if line == []:
            continue
        
        car_no, stream = line
        car_no = int(car_no)
        
        if car_no == 219:
            continue
        
        total += 1
        
        print car_no
        result = solve(stream)
        if result is not None:
            if browser is None:
                print 'login',
                browser = login()
                print 'ok'
            print 'submitting...'
            print submit_fuel(car_no, result, br=browser)
            #submit_tasks.append(pool.apply_async(submit_fuel,(car_no, result)))
            solved += 1
            
        print 'solved ', solved, '/', total
        
        print len(submit_tasks), submit_tasks
        while len(submit_tasks) > 0:
            task = submit_tasks.pop()
            try:
                print task.get(timeout=0.5)
            except TimeoutError:
                submit_tasks.append(task)
                print 'timeout'
                break
        
            
    print 'solved ', solved, '/', total
    
    for task in submit_tasks:
        print task.get()
    
    pass