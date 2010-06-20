try:
    import psyco
    psyco.full()
except ImportError:
    print "you do not have psyco, but (hopefully) it's fine"

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


def brute_force(num_gates, inputs, outputs):
    assert len(inputs) == len(outputs)
    
    for from_ in permutations(range(num_gates*2+1)):
        if eval_scheme_and_compare(from_, inputs, outputs):
            scheme = Scheme.from_permutation(from_)
            assert scheme.eval(inputs) == outputs
            return
        

if __name__ == '__main__':
    start = clock()
    #brute_force(4, [0,1,2,1], [0,1,0,1])
    
    solution = brute_force(4, server_inputs, key)
    
    if solution is not None:
        print 'Found solution'
        print solution
    else:
        print 'impossible'
        
    print 'it took', clock()-start,'seconds'