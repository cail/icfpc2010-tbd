from scheme import Scheme, key

def build_sequences(output):
    node_transitions = ('00', '02', '12', '21', '11')
    period = len(node_transitions)
    seq = []
    current_offset = 0
    for bit in output:
        for length in range(1, period + 1):
            current_offset = (current_offset + 1) % period
            if bit == node_transitions[current_offset][0]:
                break
        else: assert False, 'WTF? ' + str(output) 
        seq.append(length)
    seq.append(1) # the last fake node protects the first node from input
    return seq

def build_scheme(sequences):
    s = Scheme()
    total_cnt = sum(sequences)
    input_node = prev_start = total_cnt - sequences[-1]
    current = 0
    for length in sequences:
        last = current + length - 1
        for current in range(current, last):
            s.connect(str(current) + 'L', str(current + 1) + 'L')
            s.connect(str(current) + 'R', str(current + 1) + 'R')
        current = last
        s.connect(str(current) + 'L', str(prev_start) + 'L')
        s.connect(str(current) + 'R', str(prev_start) + 'R')
        current = last + 1
        prev_start = current - length
    s.connect(str(sequences[0] - 1) + 'L', 'X')
    s.connect('X', str(input_node) + 'L')
    #print s.to
    #print s.from_
    s.validate()
    return s

def compile_factory(output):
    seq = build_sequences(output)
    s = build_scheme(seq)
    input = [2] * len(output) # don't care
    res = s.eval(input)
    assert res == map(int, output)
    return str(s)

def fast_generate_scheme_for_fuel(suffix):
    output = ''.join(map(str,key+suffix))
    seq = build_sequences(output)
    s = build_scheme(seq)
    input = [2] * len(output) # don't care
    
    #assert res == map(int, output)
    
    pr = 10 # only test for short prefix for preformance
    res = s.eval(input[:pr])
    assert res == map(int, output)[:pr]
    return s

    
if __name__ == '__main__':
    print compile_factory('00122122211')
    
        

#sch = Scheme()
#sch.add_node(0,0)
#sch.connect('X','0L')
#    #sch.connect('0L','X')
#    #sch.connect('0R','0R')
#    
#
#    sch = Scheme.load(open("../data/sample_scheme.txt"))
#    inputs = [0,2,2,2,2,2,2,0,2,1,0,1,1,0,0,1,1] # from problem description
#
#    print sch
#    
#    outputs = list(sch.eval(inputs))
#    assert outputs == key
#    print 'in ',''.join(map(str, inputs))
#    print 'out',''.join(map(str, outputs))
