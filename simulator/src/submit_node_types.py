
from submit_fuel import *
from itertools import *

def submit_node_types():
    
    fuel = open('./data/fuel1').read()
    
    for i in product('012', repeat=3):
        i = ''.join(i)
        newfuel = fuel.replace("0#", "{0}#".format(i))
        result = submit_fuel(219, newfuel)
        print "== {0}".format(i)
        if re.search(r"unknown kind of node", result, re.S):
            pass
        else:
            print "good node!"

if __name__ == '__main__':
    submit_node_types()