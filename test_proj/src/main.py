try:
    import psyco
    psyco.full()
except ImportError:
    print "you do not have psyco, but (hopefully) it's fine"

import numpy
from pulp import *


def main():
    x = LpVariable("x", lowBound=0)
    y = LpVariable("y", lowBound=0, cat = LpInteger)
    
    problem = LpProblem("test problem", LpMinimize)
    problem += 2*x+y # objective is added first
    
    # constraints
    problem += x+y >= 0.9
    
    result = problem.solve(GLPK(msg=False))
    
    print LpStatus[result]
    
    print 'x =',value(x)
    print 'y =',value(y)

if __name__ == '__main__':
    main()
    