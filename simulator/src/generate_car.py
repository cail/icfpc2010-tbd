from random import *
from math import *
from factory_builder import fast_generate_scheme_for_fuel
from submit_car import submit_car

from car import *

def bin_search(left, right, f, eps=1e-10):
    while True:
        assert f(left) <= 0 < f(right)
        m = 0.5*(left+right)
        if right-left < eps:
            return right # approximate solution from the right
        if f(m) <= 0:
            left = m
        else:
            right = m
    
#seed(123)

def generate_car():
    n = 6
    fuel_scale = 1000
    pipe_scale = 40
    offset = 4 #pipe_scale//2
    num_chambers = 60
    
    car = Car(n)
    
    
    fuel = [randrange(1,fuel_scale) for i in range(n)]
    
    print 'fuel', fuel
    
    #d = [random()-0.5 for i in range(n)]
    
    for chamber_no in range(num_chambers):
        vec = [random()-0.5 for i in range(n)]
        
        ave = 1.0*sum(vec)/n
        for i in range(n):
            vec[i] -= ave
            
        vec_len = sqrt(sum(x*x for x in vec))
        assert vec_len > 1e-6
    
        for i in range(n):
            vec[i] /= vec_len
            
        #print vec
        
        def coeffs(alpha):
            return [int(floor(pipe_scale*(alpha+vec[i]))) for i in range(n)]
        
        def f(alpha):
            result = sum(c*log(x) for c,x in zip(coeffs(alpha), fuel))
            return result
            
        alpha = bin_search(-1e6,1e6, f)
        
        #print f(alpha)
    
        coeffs = coeffs(alpha)
        
        #print coeffs
        
        upper = []
        lower = []
        
        for i in range(n):
            up = lo = randrange(offset+1)
            if coeffs[i] > 0:
                up += coeffs[i]
            else:
                lo += -coeffs[i]
            upper += up*[i]
            lower += lo*[i]
            
            #shuffle(upper)
            #shuffle(lower)
            
        car.main_chambers.append(Chamber(upper, lower))
        
    #print car
    
    fuel = numpy_fuel(fuel)
    assert car.test_on_fuel(fuel)
    
    #print 'ok'
    #print len(car.to_stream())
    
    
   
    car_stream, perm = car.to_stream()
    
    print 'car of length', len(car_stream)
    if len(car_stream) > 22889:
        assert False, 'too long'
        
    new_fuel = [None]*n
    for i,p in enumerate(perm):
        new_fuel[p] = fuel[i]
    fuel = new_fuel
        
    
    fuel_stream = fuel_to_stream(fuel)
    print 'fuel size', len(fuel_stream)

    scheme = fast_generate_scheme_for_fuel(map(int,fuel_stream))
    
    return (car_stream, str(scheme))
    
    
    
    
if __name__ == '__main__':

    
    for i in range(600, 610):
        print 'car', i,'...'
            
        car, fuel = generate_car()
        
        print 'sending'
        result = submit_car(car, fuel)
        print 'ok'
    
        assert result.find('Good!') != -1, result

        with open("our_cars%s.txt"%i,'wt') as fout:            
            print>>fout, repr((car, fuel))
            