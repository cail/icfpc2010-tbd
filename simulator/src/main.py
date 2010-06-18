from time import clock

from numpy import array

from car import *
       

def main():
    start = clock()
    car = Car(2)
    car.main_chambers.append(Chamber([1, 0, 0], [1, 1, 0]))
    
    #fuels = [array([[1]]), array([[1]])]
    #print car.test_on_fuel(fuels)
    
    fuels = car.solveLP()
    print fuels
    #fuels = [array([[f]]) for f in fuels]
    
    print car.test_on_fuel(fuels)
    
    print 'it took', clock()-start, 'seconds'


if __name__ == '__main__':
    main()