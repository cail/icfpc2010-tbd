import psyco
psyco.full()

from random import randrange
from time import clock
from itertools import *
import sys

from scheme import Scheme, server_inputs, key

from multiprocessing import Pool


def factorial(n):
    result = 1
    for i in range(1,n+1):
        result *= i
    return result


def try_permutation((num_gates, inputs, outputs, contacts, permutation)):
    if randrange(10000) == 0:
        print permutation
        sys.stdout.flush()
    scheme = Scheme()
    for i in range(num_gates):
        scheme.add_node(i,0)
    for in_, out in zip(contacts, permutation):
        scheme.connect(in_,out) 
    if scheme.eval(inputs) == outputs:
        return scheme


def brute_force(num_gates, inputs, outputs):
    contacts = ['X'] + [str(i)+side for i in range(num_gates) for side in 'LR']
    
    pool = Pool()

    tasks = ((num_gates, inputs, outputs, contacts, p) 
             for p in permutations(contacts))
    schemes = pool.imap(try_permutation, tasks)
    
    for scheme in schemes:
        if scheme is not None:
            print 'Found solution'
            print scheme
            return scheme
        
    print 'not found'

if __name__ == '__main__':
    start = clock()
    #brute_force(4, [0,1,2,1], [0,1,0,1])
    brute_force(6, server_inputs, key)
    print 'it took', clock()-start,'seconds'