import random
import time
import re
from pprint import pprint

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
    
#for i in range(16):
#    car = '{0:b}'.format(i) + '22000010'
#    print '=' * 20 
#    print car
#    print submit_car(car, fuel)
#    pause()
#         1234567890123456789
old =    '122000010'
new =    '12222000010010010010'
new =    '221000000110'

cars = """
0 - real 0
10 - 0
110 - 1
111 - 2
112 - 3
122000 - 4
122022 - 12
12210000 - 13
12210222 - 39
122110000 - 40
122112222 - 120
1221200000 - 121
1221222222 - 363
12222000000000 - 364
12222000222222 - 1092
122220010000000 - 1093
122220012222222 - 3279
1222200200000000 - 3280
1222200222222222 - 9840
12222010000000000 - 9841
12222010222222222 - 29523
122220110000000000 - 29524
122220112222222222 - 88572
1222201200000000000 - 88573
1222201222222222222 - 265719
"""

def encode(n):
    if n == 0: return '0'
    
    

#for n in range(20):
#    print encode(n) 


# 22 = 8, 222 = 26, 2222 = 80, 22222 = 242

new = '10012222 0 00 ' + '1' * 6
new = '10012222 0 01 ' + '1' * 7
new = '10012222 0 22 ' + '1' * 14
new = '10012222 10 000 ' + '1' * 15
new = '10012222 10 222 ' + '1' * 41
new = '10012222 11 0000 ' + '1' * 42
new = '10012222 11 2222 ' + '1' * 122
new = '10012222 12 00000 ' + '1' * 123
new = '10012222 12 22222 ' + '1' * (123 + 242)
new = '10012222 22 000000000 ' + '1' * (123 + 242 + 1)

new = '10 10 10'
 
print submit_car(new, fuel)
