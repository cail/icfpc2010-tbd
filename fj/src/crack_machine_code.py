import random
import time
import re
from pprint import pprint

from submit_car import submit_car as submit_car_orig

def submit_car(car, cdr):
    print '=' * 5 + ' ' + car + ' ' + '=' * 5 
    res = submit_car_orig(car, cdr)
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
    
#for i in range(16):
#    car = '{0:b}'.format(i) + '22000010'
#    print '=' * 20 
#    print car
#    print submit_car(car, fuel)
#    pause()

print submit_car('122000010', fuel)
