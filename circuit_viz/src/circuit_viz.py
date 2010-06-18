import re
import sys


class Gate:
    
    def __init__(self, name, type, nin, nout):
        self.name = name
        self.type = type
        self.nin = nin
        self.nout = nout
    
    def __repr__(self):
        return "name:{0}, type:{1} {2}:{3}".format(self.name, self.type, self.nin, self.nout) 
        

class Circuit:
    
    def __init__(self, layout):
        
        self.parse(layout)


    def consume_target(self):
        if self.data[0] == 'X':
            self.data = self.data[1:]
            return ('X')
        m = re.match(r"(\A\d+)(L|R)", self.data)
        if m:
            self.data = self.data[len(m.group(0)) : ]
            return (m.group(1), m.group(2))
        raise Exception('cant consume target: ' + self.data[:10])
    
    def consume_type(self):
        m = re.match(r"\A\d+", self.data)
        self.data = self.data[len(m.group(0)):]
        return m.group(0)
        
        
    def consume(self, str):
        if self.data[:len(str)] != str:
            raise Exception('cant consume <'+ str + '>, data: '+ self.data[:len(str)])
        self.data = self.data[len(str):]
    
    
    def parse(self, layout):
        self.data = layout.translate(None, "\n\r\t")
        self.nodes = {}
        
        x_out = self.consume_target()
        x = Gate('X', None, None, (x_out, None))
        self.nodes[x.name] = x
        
        self.consume(':')
        cnode = 0
        while True:
            node_in_l = self.consume_target()
            node_in_r = self.consume_target()
            type = self.consume_type()
            self.consume('#')
            node_out_l = self.consume_target()
            node_out_r = self.consume_target()
            node = Gate(str(cnode), type, (node_in_l, node_in_r), (node_out_l, node_out_r))
            self.nodes[node.name] = node
            
            if self.data[0] == ':':
                self.consume(':')
                x_in = self.consume_target()
                self.nodes['X'].nin = (x_in, None)
                break
            self.consume(',')
            cnode += 1
            
        
def print_target(t):
    if len(t) == 1:
        return t[0]
    return '"'+t[0]+'":'+t[1]
        
def main():

    f = file(sys.argv[1])
    
    layout = f.read()
    c = Circuit(layout)
    
    print "// {0}".format(c.nodes)
    
    print "digraph unix {"
    print ' rank=sink; weight=1;  '
    
    for node in sorted(c.nodes.keys()):
        
        node = c.nodes[node]
                
        print '// {0}'.format(node.name)
        node_name = '"{0}" [ shape="record"'
        if node.name != 'X':
            node_name += ' label="{0}|<L> L | <R> R"'
        node_name += '];'
        print node_name.format(node.name)
        
        if node.name != 'X':
            print '"{0}":L:s -> {1}:n;'.format(node.name, print_target(node.nout[0]))
            print '"{0}":R:s -> {1}:n;'.format(node.name, print_target(node.nout[1]))
        else:
            print '"{0}":s -> {1}:n;'.format(node.name, print_target(node.nout[0]))

        print " "
    
    print "}"
    

if __name__ == '__main__':
    main()
    