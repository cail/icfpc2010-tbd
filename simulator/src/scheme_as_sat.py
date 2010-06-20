from time import clock
from random import random

from sat_solver import *
from scheme import *

class SchemeCNFBuilder(CNFBuilder):
    def new_trit(self):
        t0, t1 = self.new_vars(2)
        self.add_constraint([[-1,-2]],t0,t1)
        return t0, t1

    def new_trits(self,n):
        for i in range(n):
            yield self.new_trit()
            
    def get_constant_trit(self, value):
        return self.one*bit2sign(value%2), self.one*bit2sign(value//2)

    def add_equality_to_constant_constraint(self, vars, values):
        assert len(vars) == len(values)
        for var, value in zip(vars, values):
            self.add_constraint([[var*bit2sign(value)]])
            
    def add_inequality_constraint(self, vars1, vars2):
        assert len(vars1) == len(vars2)
        n = len(vars1)
        ne = list(self.new_vars(n))
        for i in range(n):
            self.add_constraint([[vars1[i],vars2[i],-ne[i]],
                                 [-vars1[i],-vars2[i],-ne[i]]])
        self.add_constraint([ne])


def make_table_constraint(fn):
    result = []
    for left in range(3):
        for right in range(3):
            for out in range(3):
                if fn(left,right) != out:
                    result.append([
                        -bit2sign(out%2),-bit2sign(out//2)*2,
                        -bit2sign(left%2)*3,-bit2sign(left//2)*4,
                        -bit2sign(right%2)*5,-bit2sign(right//2)*6,
                        ])
    return result


def make_multiplexor_constraint(num_bits, num_vars):
    result = []
    for i in range(2**num_bits):
        clause = [-bit2sign((i>>j)%2)*(j+2) for j in range(num_bits)]
        if i < num_vars:
            result.append(clause + [-1, i+num_bits+2])
            result.append(clause + [1, -(i+num_bits+2)])
        else:
            result.append(clause)
    return result

f0_left = make_table_constraint(
    lambda left, right: gate_function(0,left,right)[0] )
f0_right = make_table_constraint(
    lambda left, right: gate_function(0,left,right)[1] )



def time_to_reach_output(index, num_gates, can_p):
    reached = [False]*(2*num_gates+1)
    
    steps = 0
    
    while True:
        if index == 0:
            reached[index] = True
            
        for i in range(num_gates):
            left = any(reached[pin] for pin in range(2*num_gates+1) if can_p(pin, 2*i+1))
            right = any(reached[pin] for pin in range(2*num_gates+1) if can_p(pin, 2*i+2))
            reached[2*i+1] = reached[2*i+2] = left or right
            if index == 2*i+1:
                reached[index] = True
            if index == 2*i+2:
                reached[index] = True
            
        if any(reached[pin] for pin in range(2*num_gates+1) if can_p(pin, 0)):
            return steps
        steps += 1
        if steps > 2*num_gates+2:
            return 1e100
    

def hz2(num_gates, inputs, outputs, can_p=None):
    assert len(inputs) == len(outputs)
   
    print 'solving for length', len(outputs), ', numgates =', num_gates
    print '[%s]'%', '.join('*' if i is None else str(i) for i in inputs),
    print '->',outputs
    start = clock()
    
    cnf = SchemeCNFBuilder()
    
    num_pins = 2*num_gates+1
    
    brute_force_valid = can_p is None
    
    if can_p is None:
        can_p = lambda i,j: True
        
    #print_topology(num_gates, can_p)
    
    # p encodes permutation
    # p[i][j] = 1 iff this permutation maps i to j
    p = [[None]*num_pins for i in range(num_pins)]
    
    for i in range(num_pins):
        for j in range(num_pins):
            if can_p(i,j):
                p[i][j] = cnf.new_var()
    
    # totality    
    for i in range(num_pins):
        cnf.add_constraint([[p[i][j] for j in range(num_pins) if can_p(i, j)]])
        
    # injectivity
    for j in range(num_pins):
        for i1 in range(num_pins):
            for i2 in range(i1):
                if can_p(i1, j) and can_p(i2, j):
                    cnf.add_constraint([[-p[i1][j],-p[i2][j]]])
    
    values = {}
    for i in range(1, num_pins):
        values[i] = cnf.get_constant_trit(0)

    remaining_steps = len(inputs)
    
    time_to_reach_from = [time_to_reach_output(i, num_gates, can_p) 
                    for i in range(num_pins)]
    
    print time_to_reach_from

    #if None not in inputs:
    #    assert time_to_reach_from[0]+len(server_inputs) >= len(outputs), \
    #        "we don't know enough server inputs"

    input_vars = []            
    for input, output in zip(inputs, outputs):
        remaining_steps -= 1
        if time_to_reach_from[0] > remaining_steps:
            values[0] = None
        else:
            if input is not None:
                values[0] = cnf.get_constant_trit(input)
            else:
                values[0] = cnf.new_trit()
        input_vars.append(values[0])
        
        new_values = {}
        for i in range(1, num_pins):
            if time_to_reach_from[i] > remaining_steps:
                new_values[i] = None
            else:
                new_values[i] = cnf.new_trit()

        def multiplex_trit(index, result, trits):
            for i in range(num_pins):
                if can_p(i, index):
                    cnf.add_constraint([[-p[i][index], result[0], -trits[i][0]]])
                    cnf.add_constraint([[-p[i][index], -result[0], trits[i][0]]])
                    cnf.add_constraint([[-p[i][index], result[1], -trits[i][1]]])
                    cnf.add_constraint([[-p[i][index], -result[1], trits[i][1]]])
        
        for i in range(num_gates):
            if time_to_reach_from[2*i+1] > remaining_steps or\
                time_to_reach_from[2*i+2] > remaining_steps:
                continue
            # multiplex
            left_in = cnf.new_trit()
            right_in = cnf.new_trit()
            
            multiplex_trit(2*i+1, left_in, values)
            multiplex_trit(2*i+2, right_in, values)
            
            left_out = new_values[2*i+1]
            right_out = new_values[2*i+2]
            
            cnf.add_constraint(f0_left, *left_out+left_in+right_in)
            cnf.add_constraint(f0_right, *right_out+left_in+right_in)
            
            values[2*i+1] = left_out
            values[2*i+2] = right_out
                        
        multiplex_trit(0, cnf.get_constant_trit(output), values)    
    
    print cnf.num_vars,'vars'
    print len(cnf.clauses), 'clauses'
    
    cnf.solve()
    
    print 'it took', clock()-start,'seconds'
    print 'problem is ', 'sat' if cnf.satisfiable else 'unsat'
    print
    
    if cnf.satisfiable:
        pins = pin_names(num_gates)
        
        scheme = Scheme()
        for i in range(num_gates):
            scheme.add_node(i, 0)
        
        for i in range(num_pins):
            for j in range(num_pins):
                if can_p(i,j) and cnf.value(p[i][j]) == 1:
                    scheme.connect(pins[i], pins[j])
        
        for i, iv in enumerate(input_vars):
            if iv is not None:
                inputs[i] = cnf.value(*iv)
            else:
                inputs[i] = 0
            
        assert scheme.eval(inputs) == outputs
        
        for i, iv in enumerate(input_vars):
            if iv is None:
                inputs[i] = None
                
        return scheme
        
    else:
        if brute_force_valid and num_gates <= 3:
            from scheme_brute_force import brute_force
            assert brute_force(num_gates, inputs, outputs) is None

def print_topology(num_gates, can_p):
    for i in range(2*num_gates+1):
        for j in range(2*num_gates+1):
            if can_p(i,j):
                print '+',
            else:
                print '.',
        print

def generate_scheme(outputs):
    
    if len(outputs) <= len(server_inputs):
        for num_gates in range(0, 5):
            result = hz2(num_gates, server_inputs[:len(outputs)], outputs)
            if result is not None:
                return result
        print 'we fail'
        #return
    
    postprocessor = 3
    num_layers = 6
    layer_size = 1
    
    num_gates = postprocessor+num_layers*layer_size
    
    def can_p(i,j):
        gate1 = (i-1)//2
        gate2 = (j-1)//2
        
        layer1 = (gate1-postprocessor)//layer_size
        layer2 = (gate2-postprocessor)//layer_size
        
        if i == 0:
            return layer2 == num_layers-1
        
        if 0 <= gate1 < postprocessor:
            if 0 <= gate2 < postprocessor:
                return True
                return gate2 >= gate1
            return j == 0 or layer2 == num_layers-1 or 0 <= gate2 < postprocessor
        if layer1 == 0:
            return 0 <= gate2 < postprocessor
        return layer1 >= 0 and (layer1 == layer2+1)
        
    print_topology(num_gates, can_p)
    
    inputs = [None]*len(outputs)
    result = hz2(num_gates, inputs, outputs, can_p=can_p)
    print 'result found'
    significant_part = inputs[:inputs.index(None)]
    print 'on significant inputs', significant_part
    print
    
    q = generate_scheme(significant_part)
    print ''
    
    q.append(result)
    return q # composed with result
        

def generate_scheme_for_fuel(suffix):
    result = generate_scheme(key+suffix)
    assert result.eval(server_inputs+[0 for q in suffix]) == key+suffix
    return result


if __name__ == '__main__':
    
    

    start = clock()

    suffix = [1,1,1,1,0]
    suffix = []
    
    result = generate_scheme_for_fuel(suffix)
    
    #result = generate_scheme([2])
    
    if result is not None:
        print 'found solution with',result.num_nodes,'gates'
        print result
    else:
        print 'impossible' 
        
    print 'it took', clock()-start, 'seconds'    
    #multiplexor_constr = make_multiplexor_constraint(3,5)
    
    
    #exit()
    
    
    
    
    
    #cnf.solve()
    #if cnf.satisfiable:
    #    print cnf.value(*x), cnf.value(*y), cnf.value(*z)
    #else:
    #    print "can't solve"