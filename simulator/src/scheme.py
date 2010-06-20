import re


__all__ = [
    'pin_names',
    'gate_values',
    'gate_function',
    'gate_dict',
    'Scheme',
    'eval_scheme',
    'eval_scheme_and_compare',
    'server_inputs',
    'key',
]



def pin_names(num_gates):
    return ['X'] + [str(i)+side for i in range(num_gates) for side in 'LR']

def parse_pin(e):
    assert e != 'X'
    m = re.match(r"(\d+)(L|R)", e)
    return (int(m.group(1)), m.group(2))


gate_values =\
[
   [[(0,2),(2,2),(1,2)],
    [(1,2),(0,0),(2,1)],
    [(2,2),(1,1),(0,0)]],
] 


def gate_function(fn, left, right):
    return gate_values[fn][left][right]

gate_dict = dict(((left, right), gate_function(0, left, right))
                 for left in range(3) for right in range(3))

class Scheme(object):
    __slots__ = [
        'to',
        'from_',
        'num_nodes',
        'function',
        ]
    
    @staticmethod
    def load(lines):
        text = "".join(line.strip() for line in lines)
        scheme = Scheme()
        
        input, gates, output = text.split(':')
        pin_re = r"(X|\d+(?:L|R))"
        assert re.match(pin_re, input)
        assert re.match(pin_re, output)
        
        scheme.connect('X', input)
        scheme.connect(output, 'X')
        
        gates = gates.split(',')
        for i,gate in enumerate(gates):
            m = re.match(pin_re*2+r"(\d+)#"+pin_re*2+"$", gate)
            leftIn, rightIn, function, leftOut, rightOut = m.groups()
            
            scheme.add_node(i, int(function))
            
            scheme.connect(leftIn, str(i)+'L')
            scheme.connect(rightIn, str(i)+'R')
        
        assert str(scheme).replace('\n','') == text
        return scheme
    
    @staticmethod
    def from_permutation(from_):
        scheme = Scheme()
        pins = pin_names(len(from_)//2)
        for i in range(len(from_)//2):
            scheme.add_node(i, 0)
        for to, fr in enumerate(from_):
            scheme.connect(pins[fr], pins[to])
        return scheme
    
    def get_permutation(self):
        pins = pin_names(self.num_nodes)
        from_ = [None]*len(pins)
        for k,v in self.from_.items():
            from_[pins.index(k)] = pins.index(v)
        return from_
    
    def __init__(self):
        self.num_nodes = 0
        self.to = {}
        self.from_ = {}
        self.function = {}
        
    def add_node(self, n, fn):
        self.num_nodes = max(self.num_nodes, n+1)
        self.function[n] = fn
        
    def connect(self, pin1, pin2):
        for pin in [pin1, pin2]:
            if pin == 'X':
                continue
            n, side = parse_pin(pin)
            self.num_nodes = max(self.num_nodes, n+1)
        self.to[pin1] = pin2
        self.from_[pin2] = pin1

    def __str__(self):
        result = []
        result.append(self.to['X']+':')
        for i in range(self.num_nodes):
            s = (self.from_[str(i)+'L']+self.from_[str(i)+'R']+
                 str(self.function[i])+'#'+
                 self.to[str(i)+'L']+self.to[str(i)+'R'])
            if i == self.num_nodes-1:
                s += ':'
            else:
                s += ','
            result.append(s)
        result.append(self.from_['X'])
        
        return '\n'.join(result)
    
    def naive_eval(self, inputs):
        result = []
        values = {}
        for i in range(self.num_nodes):
            values[str(i)+'L'] = 0
            values[str(i)+'R'] = 0
            
        for input in inputs:
            values['X'] = input
            for i in range(self.num_nodes):
                values[str(i)+'L'], values[str(i)+'R'] =\
                    gate_function(self.function[i],
                                  values[self.from_[str(i)+'L']],
                                  values[self.from_[str(i)+'R']])
            result.append( values[self.from_['X']] )
        return result
    
    def eval(self, inputs):
        result = eval_scheme(self.get_permutation(), inputs)
        assert result == self.naive_eval(inputs)
        return result


table = []
for i in range(3):
    for j in range(3):
        left, right = gate_function(0,i,j)
        table.append(left)
        table.append(right)

def simulation_step(values, from_, input):
    local_table = table
    values[0] = input
    for i in range(len(from_)//2):
        left_in = values[from_[2*i+1]]
        right_in = values[from_[2*i+2]]
        left_out = local_table[left_in*6+right_in*2]
        right_out = local_table[left_in*6+right_in*2+1]
        values[2*i+1] = left_out
        values[2*i+2] = right_out
    return values[from_[0]]
       
def eval_scheme(from_, inputs):
    outputs = []
    
    values = [0]*len(from_)
    for input in inputs:
        outputs.append(simulation_step(values, from_, input))
    
    return outputs

def eval_scheme_and_compare(from_, inputs, outputs):
    values = [0]*len(from_)
    for input,output in zip(inputs, outputs):
        if simulation_step(values, from_, input) != output:
            return False
    
    return True
            

server_inputs = map(int,'01202101210201202')
key = map(int,'11021210112101221')
 
        
if __name__ == '__main__':
    #sch = Scheme()
    #sch.add_node(0,0)
    #sch.connect('X','0L')
    #sch.connect('0L','X')
    #sch.connect('0R','0R')
    

    sch = Scheme.load(open("../data/sample_scheme.txt"))
    inputs = [0,2,2,2,2,2,2,0,2,1,0,1,1,0,0,1,1] # from problem description

    print sch
    
    outputs = list(sch.eval(inputs))
    assert outputs == key
    print 'in ',''.join(map(str, inputs))
    print 'out',''.join(map(str, outputs))
