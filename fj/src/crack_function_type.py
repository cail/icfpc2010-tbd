from itertools import izip_longest
from pprint import pprint

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def fuction_generator(constraints):
    """
    constraints is a dictionary of pairs of the form (0, 0):(0, 2) 
    """
    current = [0] * 18
    # convert constraints
    tmp = {}
    for k, v in constraints:
        i = (k[0] * 3 + k[1]) * 2
        tmp[i] = v[0]
        tmp[i + 1] = v[1]
    constraints = tmp
    while True:
        for i in range(18):
            if i in constraints: continue
            k = current[i] + 1
            current[i] = k % 3
            if k != 3: break
        else:
            return
        # assemble the factory
        tmp = {}
        for i, v in enumerate(grouper(2, current)):
            tmp[(i / 3, i % 3)] = v
        yield tmp

#constraints = {(0, 0):(0, 2)
#pprint(take(function_generator(

def format_factory(template):
    print template
    max_state = len(template) - 1
    if template[max_state] != 'x':
        start = '0L:X%dR0#' % max_state
        end = 'X0R:%dL' % max_state
    else:
        start = '0L:X%dL0#' % max_state
        end = '0RX:%dR' % max_state
    core = ''
    for i in range(0, max_state):
        if template[i] != 'x':
            core += '%dL%dR,%dL%dR0#' % (i + 1, i + 1, i, i)
        else:
            core += '%dR%dL,%dR%dL0#' % (i + 1, i + 1, i, i)
    return start + core + end


def format_straight_factory_L(n):
    return format_factory('-' * n)

def format_straight_factory_R(n):
    return format_factory('-' * (n - 1) + 'x')

def execute_LL(f, input): # 0L:X0R0#X0R:0L -- 02120112100002120 
    l, r = 0, 0
    for i in input:
        l, r = f(i, r)
        yield l

def execute_RL(f, input): # 0R:0RX0#X0L:0L -- 01210221200001210 
    l, r = 0, 0
    for i in input:
        l, r = f(r, i)
        yield l

def execute_LR(f, input): # 0L:X0L0#0RX:0R -- 22120221022022120
    l, r = 0, 0
    for i in input:
        l, r = f(i, l)
        yield r

def execute_RR(f, input): # 0R:0LX0#0LX:0R -- 22022022022022022
    l, r = 0, 0
    for i in input:
        l, r = f(l, i)
        yield r

def parse(s):
    return map(int, s)

def unparse(lst):
    return ''.join(map(str, lst))

def function_from_table(table):
    def f(*x):
        return table[x]
    return f
    
def parse_table(s):
    table = {}
    lines = filter(None, (l.strip() for l in s.split('\n')))
    for l in lines:
        a, b = (s.strip() for s in l.split(':'))
        assert len(a) == len(b) == 2
        table[tuple(parse(a))] = tuple(parse(b))
    return table
    
table_template = """
00 : 02
02 : 12
11 : 00
12 : 21
20 : 22
21 : 11
22 : 00

01 : %d2
10 : %d2
"""

input = parse('01202101210201202')
for a in range(3):
    for b in range(3):
        f = function_from_table(parse_table(table_template % (a, b)))
        print a, b, unparse(execute_RL(f, input))
        

#for n in range(1, 7):
#    print format_factory('-' * n), ' -- '
#    print format_factory('-' * (n - 1) + 'x'), ' -- '
#    print '00 : 00'
#    print
#
#for n in range(1, 4):
#    print format_factory('x' + '-' * n), ' -- '
#    print format_factory('x' + '-' * (n - 1) + 'x'), ' -- '
#    print '00 : 00'
#    print

