from random import randrange
from collections import namedtuple

from numpy import *


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

    def __init__(self, num_tanks):
        self.num_tanks = num_tanks
        self.main_chambers = []
        self.aux_chambers = []

    def testOnInput(self, fuels, input):
        n = len(input)
        for chamber in self.main_chambers:
            if not testChamberOnInput(chamber, input, main=True):
                return False
        for chamber in self.aux_chambers:
            if not testChamberOnInput(chamber, input, main=False):
                return False
        return True

    def testFuel(self, fuels, num_tests=100):
        assert len(fuels) == self.num_tanks
        
        n = fuels[0].shape[0]
        assert all(f.shape == (n, n) for f in fuels)

        for i in range(num_tests):
            input = array([randrange(10) for i in n], dtype=int)
            input[0] += 1
            if not self.testOnInput(input):
                return False
        return True
        

def pipeFunction(pipe, fuels, input):
    x = input
    for section in pipe:
        x = dot(fuels[section], x)
    return x


def testChamberOnInput(chamber, fuels, input, main):
    n = len(fuels)
    assert input.shape == (n,)
    upper = pipeFunction(chamber.upper, fuels, input)
    lower = pipeFunction(chamber.lower, fuels, input)
    
    return all(up >= lo for up, lo in zip(upper, lower)) and \
        (not main or upper[0] > lower[0])


        

def main():
    pass

if __name__ == '__main__':
    main()