from submit_car import submit_car
import random
import time
from pprint import pprint

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

for i in range(16):
    car = '{0:b}'.format(i) + '22000010'
    print '=' * 20 
    print car
    print
    print submit_car(car, fuel)
    pause()
    print
    print

