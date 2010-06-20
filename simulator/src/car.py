from random import randrange
from collections import namedtuple

from numpy import dot, array, ndarray

from tstream_parser import parse_chambers
from tstream_composer import compose_matrices

__all__ = [
    'Car',
    'Chamber',
    'fuel_to_stream',
]

def fuel_to_stream(fuel):
    if not isinstance(fuel[0], ndarray):
        fuel = [array([[f]]) for f in fuel]
    
    q = []
    for f in fuel:
        q.append(list(map(list,f)))
    
    return compose_matrices(q)
    

Chamber = namedtuple('Chamber', 'upper lower')

class Car(object):
    # ***_chamers is list of Chambers
    # each chamber is named tuple of two lists (pipes)
    # each pipe is list of integer (tank numbers starting from 0)
    
    __slots__ = [
        'num_tanks',
        'main_chambers',
        'aux_chambers',
        'representation',
        ]

    @staticmethod
    def from_stream(s):
        assert isinstance(s,basestring)
        car = Car(0)
        car.representation = s
        chambers = parse_chambers(iter(s))
        t = 0
        for flag, up, low in chambers:
            t = max([t]+up+low)
            if flag == 0:
                car.main_chambers.append(Chamber(up, low))
            elif flag == 1:
                car.aux_chambers.append(Chamber(up, low))
            else:
                assert False
        car.num_tanks = t+1
        return car
    
    def to_stream(self):
        raise NotImplementedError()
    
    def __str__(self):
        return "Car(%s,\n  %s,\n  %s)"%(self.num_tanks, self.main_chambers, self.aux_chambers)

    def __init__(self, num_tanks):
        self.num_tanks = num_tanks
        self.main_chambers = []
        self.aux_chambers = []
        
    def all_chambers(self):
        for chamber in self.main_chambers:
            yield chamber, True
        for chamber in self.aux_chambers:
            yield chamber, False

    def test_on_input(self, fuel, input):
        n = len(input)
        for chamber, isMain in self.all_chambers():
            if not test_chamber_on_input(chamber, fuel, input, main=isMain):
                return False
        return True

    def test_on_fuel(self, fuel):
        """
        fuel is list of either numpy 2d arrays or just integers (for 1d case)
        """
        assert len(fuel) == self.num_tanks

        if isinstance(fuel[0], ndarray):        
            n = fuel[0].shape[0]
            assert all(f.shape == (n, n) for f in fuel)
        else:
            n = 1
            assert all(isinstance(f, (int, long)) for f in fuel), fuel

        #if n == 1:
            # that's enough to ensure validity of the fuel
        #    num_tests = 1
        
        for i in range(n):
            input = [0 for i in range(n)]
            input[0] = 1
            input[i] = 1
            if not self.test_on_input(fuel, input):
                return False
        return True
        

def pipe_function(pipe, fuel, input):
    if not isinstance(fuel[0], ndarray):
        assert len(input) == 1
        x = input[0]
        for section in pipe:
            x *= fuel[section]
        return [x]
    
    if not isinstance(input, ndarray):
        input = array(input, dtype=int)
        
    for section in pipe:
        input = dot(fuel[section], input)
    return input


def test_chamber_on_input(chamber, fuel, input, main):
    n = len(input)
    upper = pipe_function(chamber.upper, fuel, input)
    lower = pipe_function(chamber.lower, fuel, input)
    
    return all(up >= lo for up, lo in zip(upper, lower)) and \
        (not main or upper[0] > lower[0])


if __name__ == '__main__':
    car = Car.from_stream('122221001200000000000000000000010')
    
    print car
    