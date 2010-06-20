from time import clock

from numpy import array


from car import *
from solve_lp import *
from solve_brute_force import *
       

def main():
    start = clock()
    car = Car(2)
    car.main_chambers.append(Chamber([1, 0, 0], [1, 1, 0]))
    
    #fuel = [array([[1]]), array([[1]])]
    #print car.test_on_fuel(fuel)
    
    fuel = solve_LP(car)
    print fuel, car.test_on_fuel(fuel)
    
    fuel = solve_brute_force(car)
    print fuel, car.test_on_fuel(fuel)
    
    
    print 'it took', clock()-start, 'seconds'


if __name__ == '__main__':
    main()