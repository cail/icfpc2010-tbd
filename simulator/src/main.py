from random import randrange
from collections import namedtuple

from numpy import dot, array
from pulp import *



Chamber = namedtuple('Chamber','upper lower')


class Car(object):
    __slots__ = [
        'num_tanks',
        'main_chambers',
        'aux_chambers',
        ]
    # ***_chamers is list of Chambers
    # each chamber is named tuple of two lists (pipes)
    # each pipe is list of integer (tank numbers starting from 0)
    
    # fuels is list of numpy 2d arrays (preferably with dtype=int)

    def __init__(self, num_tanks):
        self.num_tanks = num_tanks
        self.main_chambers = []
        self.aux_chambers = []
        
    def all_chambers(self):
        for chamber in self.main_chambers:
            yield chamber, True
        for chamber in self.aux_chambers:
            yield chamber, False

    def testOnInput(self, fuels, input):
        n = len(input)
        for chamber in self.main_chambers:
            if not testChamberOnInput(chamber, fuels, input, main=True):
                return False
        for chamber in self.aux_chambers:
            if not testChamberOnInput(chamber, fuels, input, main=False):
                return False
        return True

    def testOnFuel(self, fuels, num_tests=100):
        assert len(fuels) == self.num_tanks
        
        n = fuels[0].shape[0]
        assert all(f.shape == (n, n) for f in fuels)

        for i in range(num_tests):
            input = array([randrange(10) for i in range(n)], dtype=int)
            input[0] += 1
            if not self.testOnInput(fuels, input):
                return False
        return True
    
    def solveLP(self):
        # since we are in logspace, all variables should be strictly positive
        
        eps = 1
        vars = [LpVariable('x%d'%i, lowBound=eps, cat=LpInteger) 
                for i in range(self.num_tanks)]
        problem = LpProblem('search for fuel', LpMinimize)
        problem += lpSum(vars)
        
        for chamber, isMain in self.all_chambers():
            coeffs = [0]*self.num_tanks
            for i in chamber.upper:
                coeffs[i] += 1
            for i in chamber.lower:
                coeffs[i] -= 1
            # i'm not doing it as difference of lpSums because it's buggy
            term = lpSum(coeff*var for coeff, var in zip(coeffs, vars))
            if isMain:
                problem += term >= eps
            else:
                problem += term >= 0
        
        #print problem
        
        result = problem.solve(GLPK(msg=False))
        
        #print LpStatus[result]
        #for v in vars:
        #    print v,'=', value(v)
            
        assert result == LpStatusOptimal
        
        # go back from logspace to linear space
        return [2**value(v) for v in vars]
        
        

def pipeFunction(pipe, fuels, input):
    x = input
    for section in pipe:
        x = dot(fuels[section], x)
    return x


def testChamberOnInput(chamber, fuels, input, main):
    n, = input.shape
    upper = pipeFunction(chamber.upper, fuels, input)
    lower = pipeFunction(chamber.lower, fuels, input)
    
    return all(up >= lo for up, lo in zip(upper, lower)) and \
        (not main or upper[0] > lower[0])

        

def main():
    car = Car(2)
    car.main_chambers.append(Chamber([1, 0, 0, 1], [0, 1, 0]))
    
    #fuels = [array([[1]]), array([[2]])]
    #print car.testOnFuel(fuels)
    
    fuels = car.solveLP()
    print fuels
    fuels = [array([[f]]) for f in fuels]
    print car.testOnFuel(fuels)


if __name__ == '__main__':
    main()