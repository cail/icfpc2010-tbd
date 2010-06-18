from random import randrange
from collections import namedtuple

from numpy import dot, array, ndarray
from pulp import *


__all__ = [
    'Car',
    'Chamber',
]

Chamber = namedtuple('Chamber','upper lower')


class Car(object):
    # ***_chamers is list of Chambers
    # each chamber is named tuple of two lists (pipes)
    # each pipe is list of integer (tank numbers starting from 0)
    
    __slots__ = [
        'num_tanks',
        'main_chambers',
        'aux_chambers',
        ]

    @staticmethod
    def from_stream(self, s):
        raise NotImplementedError()
    
    def to_stream(self):
        raise NotImplementedError()

    def __init__(self, num_tanks):
        self.num_tanks = num_tanks
        self.main_chambers = []
        self.aux_chambers = []
        
    def all_chambers(self):
        for chamber in self.main_chambers:
            yield chamber, True
        for chamber in self.aux_chambers:
            yield chamber, False

    def test_on_input(self, fuels, input):
        n = len(input)
        for chamber, isMain in self.all_chambers():
            if not test_chamber_on_input(chamber, fuels, input, main=isMain):
                return False
        return True

    def test_on_fuel(self, fuels, num_tests=100):
        """
        fuels is list of either numpy 2d arrays or just integers (for 1d case)
        """
        assert len(fuels) == self.num_tanks

        if isinstance(fuels[0], ndarray):        
            n = fuels[0].shape[0]
            assert all(f.shape == (n, n) for f in fuels)
        else:
            n = 1
            assert all(isinstance(f, int) for f in fuels)

        if n == 1:
            # that's enough to ensure validity of the fuel
            num_tests = 1
        
        for i in range(num_tests):
            input = [randrange(100) for i in range(n)]
            input[0] += 1
            if not self.test_on_input(fuels, input):
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
            assert len(term) != 0, 'pipes are equivalent'
            if isMain:
                problem += term >= eps
            else:
                problem += term >= 0
        
        result = problem.solve(GLPK(msg=False))
        
        if result != LpStatusOptimal:
            print problem
            result = problem.solve(GLPK(msg=True))
            print LpStatus[result]
            assert False
        
        # go back from logspace to linear space
        return [2**value(v) for v in vars]
        
        

def pipe_function(pipe, fuels, input):
    if not isinstance(fuels[0], ndarray):
        assert len(input) == 1
        x = input[0]
        for section in pipe:
            x *= fuels[section]
        return [x]
    
    if isinstance(input, list):
        input = array(input, dtype=int)
        
    for section in pipe:
        input = dot(fuels[section], input)
    return input


def test_chamber_on_input(chamber, fuels, input, main):
    n = len(input)
    upper = pipe_function(chamber.upper, fuels, input)
    lower = pipe_function(chamber.lower, fuels, input)
    
    return all(up >= lo for up, lo in zip(upper, lower)) and \
        (not main or upper[0] > lower[0])
