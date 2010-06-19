from time import clock

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

def hz(cnf, num_gates, inputs, outputs):
    n = 0
    while 2**n < 2*num_gates+1:
        n += 1
        
    multiplexor = make_multiplexor_constraint(n, 2*num_gates+1)

    from_ = []
    for i in range(2*num_gates+1):
        from_.append(list(cnf.new_vars(n)))
    for i in range(2*num_gates+1):
        for j in range(i):
            cnf.add_inequality_constraint(from_[i], from_[j]);
    #print 'from:',from_

    values = [None]+list(cnf.new_trits(2*num_gates))
    for value in values[1:]:
        cnf.add_equality_to_constant_constraint(value, [0,0])
    #print 'values:', values
    
    for input, output in zip(inputs, outputs):
        values[0] = cnf.new_trit()
        cnf.add_equality_to_constant_constraint(values[0], [input%2, input//2])
        
        for i in range(num_gates):
            left_in, right_in = cnf.new_trits(2)
            
            for j in range(2):
                cnf.add_constraint(multiplexor, 
                                   left_in[j], # result
                                   *from_[2*i+1]+    # index 
                                   [v[j] for v in values] #values
                                   )
                cnf.add_constraint(multiplexor, 
                                   right_in[j], # result
                                   *from_[2*i+2]+    # index 
                                   [v[j] for v in values] #values
                                   )
            
            left_out, right_out = cnf.new_trits(2)
            
            cnf.add_constraint(f0_left,*left_out+left_in+right_in)
            cnf.add_constraint(f0_right,*right_out+left_in+right_in)
            
            values[2*i+1] = left_out
            values[2*i+2] = right_out
            
            output_trit = cnf.new_trit()
            for j in range(2):
                cnf.add_constraint(multiplexor, 
                                   output_trit[j], # result
                                   *from_[0]+    # index 
                                   [v[j] for v in values] #values
                                   )
        cnf.add_equality_to_constant_constraint(output_trit, [output%2, output//2])
    
    print cnf.num_vars,'vars'
    print len(cnf.clauses), 'clauses'
    #pprint(cnf.clauses)

    cnf.solve()
    #cnf.print_solution()
    
    if cnf.satisfiable:
        pins = pin_names(num_gates)
        
        scheme = Scheme()
        for i in range(num_gates):
            scheme.add_node(i, 0)
        for to, f in enumerate(from_):
            f = cnf.value(*f)
            scheme.connect(pins[f], pins[to])
            
        assert scheme.eval(inputs) == outputs
        return scheme
        
    else:
        if num_gates <= 3:
            from scheme_brute_force import brute_force
            assert brute_force(num_gates, inputs, outputs) is None
     

#def make_cnf_for_scheme(input):

def hz2(cng, num_gates, inputs, outputs, can_p=None):
    assert len(inputs) == len(outputs)
    
    num_pins = 2*num_gates+1
    
    brute_force_valid = can_p is None
    
    if can_p is None:
        can_p = lambda i,j: True
    
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
        
    for input, output in zip(inputs, outputs):
        values[0] = cnf.get_constant_trit(input)
        
        new_values = {}
        for i in range(1, num_pins):
            new_values[i] = cnf.new_trit()

        def multiplex_trit(index, result, trits):
            for i in range(num_pins):
                if can_p(i, index):
                    cnf.add_constraint([[-p[i][index], result[0], -trits[i][0]]])
                    cnf.add_constraint([[-p[i][index], -result[0], trits[i][0]]])
                    cnf.add_constraint([[-p[i][index], result[1], -trits[i][1]]])
                    cnf.add_constraint([[-p[i][index], -result[1], trits[i][1]]])
        
        for i in range(num_gates):
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
    #cnf.print_solution()
    
    if cnf.satisfiable:
        pins = pin_names(num_gates)
        
        scheme = Scheme()
        for i in range(num_gates):
            scheme.add_node(i, 0)
        
        for i in range(num_pins):
            for j in range(num_pins):
                if can_p(i,j) and cnf.value(p[i][j]) == 1:
                    scheme.connect(pins[i], pins[j])
            
        assert scheme.eval(inputs) == outputs
        return scheme
        
    else:
        if brute_force_valid and num_gates <= 3:
            from scheme_brute_force import brute_force
            assert brute_force(num_gates, inputs, outputs) is None


if __name__ == '__main__':
    
    cnf = SchemeCNFBuilder()

    start = clock()
    prefix_len = 17
    
    can_p = None
    can_p = lambda i, j: abs(i-j) < 6
    
    result = hz2(cnf, 8, server_inputs[:prefix_len], key[:prefix_len], can_p=can_p)
    
    if result is not None:
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