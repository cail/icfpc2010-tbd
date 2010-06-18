import re

special_contact = 'X'

def parse_contact(e):
    assert e != special_contact
    m = re.match("(\d)+(L|R)", e)
    return (int(m.group(1)), m.group(2))

class Scheme(object):
    __slots__ = [
        'to',
        'from_',
        'num_nodes',
        'function',
        ]
    
    def __init__(self):
        self.num_nodes = 0
        self.to = {}
        self.from_ = {}
        self.function = {}
        
    def add_node(self, n, fn):
        self.num_nodes = max(self.num_nodes, n+1)
        self.function[n] = fn
        
    def connect(self, e1, e2):
        for e in [e1, e2]:
            if e == special_contact:
                continue
            n, side = parse_contact(e)
            self.num_nodes = max(self.num_nodes, n+1)
        self.to[e1] = e2
        self.from_[e2] = e1

    def __str__(self):
        result = []
        result.append(self.to[special_contact]+':')
        for i in range(self.num_nodes):
            s = (self.from_[str(i)+'L']+self.from_[str(i)+'R']+
                 str(self.function[i])+'#'+
                 self.to[str(i)+'L']+self.to[str(i)+'R'])
            if i == self.num_nodes-1:
                s += ':'
            else:
                s += ','
            result.append(s)
        result.append(self.from_[special_contact])
        
        return '\n'.join(result)

if __name__ == '__main__':
    sch = Scheme()
    sch.add_node(0,0)
    sch.add_node(1,0)
    sch.connect('X','0L')
    sch.connect('0L','X')
    sch.connect('0R','0R')
    sch.connect('1L','1R')
    sch.connect('1R','1L')
    
    print sch
