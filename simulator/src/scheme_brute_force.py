import psyco
psyco.full()

from random import randrange, shuffle
from time import clock
from itertools import *
import sys

from scheme import *

from multiprocessing import Pool


def factorial(n):
    result = 1
    for i in range(1,n+1):
        result *= i
    return result


def try_permutation((num_gates, inputs, outputs, pins, permutation)):
    #if randrange(10000) == 0:
    #    print permutation
    #    sys.stdout.flush()
    scheme = Scheme()
    for i in range(num_gates):
        scheme.add_node(i,0)
    for in_, out in zip(pins, permutation):
        scheme.connect(in_,out)
     
    if outputs == scheme.eval(inputs):
        return scheme


def brute_force(num_gates, inputs, outputs):
    assert len(inputs) == len(outputs)
    pins = pin_names(num_gates)
    
    pool = Pool()

    pc = pins
    shuffle(pins)
    
    tasks = ((num_gates, inputs, outputs, pins, p) 
             for p in permutations(pc))
    schemes = pool.imap(try_permutation, tasks)
    
    for scheme in schemes:
        if scheme is not None:
            return scheme
        

if __name__ == '__main__':
    start = clock()
    #brute_force(4, [0,1,2,1], [0,1,0,1])
    
    solution = brute_force(6, server_inputs, key)
    
    if solution is not None:
        print 'Found solution'
        print solution
    else:
        print 'impossible'
        
    print 'it took', clock()-start,'seconds'