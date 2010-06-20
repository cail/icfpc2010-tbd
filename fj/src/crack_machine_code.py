import random
import time
import re
from pprint import pprint
from itertools import ifilter
from tstream_parser import parse_number, parse_chambers, parse_matrices
from tstream_composer import compose_number, compose_row, compose_matrix, compose_matrices

from submit_car import submit_car as submit_car_orig

def submit_car(car, cdr):
    print '=' * 5 + ' ' + car + ' ' + '=' * 5 
    res = submit_car_orig(car.replace(' ', ''), cdr)
    return re.sub(r'^\s*circuit output starts with\s*[012]*\s*this is a legal prefix\s*', '', res)
    

fuel = """
0R:
1LX0#2L1L,
0R3L0#0L2R,
0L1R0#X3R,
5L2R0#1R4L,
3R4R0#6R4R,
7R7L0#3L7L,
6R4L0#7R6L,
5R6L0#5R5L:
2L
"""

def pause():
    time.sleep(1.0  + random.random())
    
def clean_stream(s):
    return ifilter(lambda c: c in '012', s)

numbers = """
0 - 0
10 - 1
11 - 2
12 - 3
22000 - 4
22022 - 12
2210000 - 13
2210222 - 39
22110000 - 40
22112222 - 120
221200000 - 121
221222222 - 363
2222000000000 - 364
2222000222222 - 1092
22220010000000 - 1093
22220012222222 - 3279
222200200000000 - 3280
222200222222222 - 9840
2222010000000000 - 9841
2222010222222222 - 29523
22220110000000000 - 29524
22220112222222222 - 88572
222201200000000000 - 88573
222201222222222222 - 265719
"""
numbers = filter(None, (s.strip() for s in numbers.split('\n')))
numbers = [(src.strip(), int(ref)) for src, ref in (s.split('-') for s in numbers)] 


def test_parse_number():
    for src, ref in numbers:
        assert parse_number(clean_stream(src)) == ref
    print 'parse_number works, yay!' 
       
def test_compose_number():
    for src, ref in numbers:
        assert compose_number(ref) == src
    print 'compose_number works, yay!' 

test_parse_number()
test_compose_number()
#pprint(parse_chambers(clean_stream('')))

s = compose_matrices([[[1, 1],
       [0, 0]], [[1, 0],
       [0, 0]], [[1, 1],
       [0, 0]]])
print len(s), s

#print submit_car(new, fuel)
print parse_matrices(iter('22102202201011220002202201002200022022010022000'))