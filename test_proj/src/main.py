try:
    import psyco
    psyco.full()
except ImportError:
    print "you do not have psyco, but (hopefully) it's fine"

import numpy
from pulp import *


def main():
    x = LpVariable("x")
    y = LpVariable("y")
    
    problem = LpProblem("test problem", LpMinimize)
    problem += x <= 2
    problem += x+y >= 1
    
    result = problem.solve(GLPK(msg=False))
    
    print LpStatus[result]
    
    print 'x =',value(x)
    print 'y =',value(y)

if __name__ == '__main__':
    main()
    
# test modification
# test modification 2