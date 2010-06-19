import re
import sys
from scheme import Scheme, parse_pin
        
def print_viz(e):
    if e == 'X':
        return 'X'
    n, side = parse_pin(e)
    return '"{0}":{1}'.format(n, side)
        
def main():

    s = Scheme.load(open(sys.argv[1]))
    
    print "// {0}".format(str(s).translate(None, '\r\n'))
    
    print "digraph unix {"
    print ' rank=sink; weight=1;  '

    for node in ['X'] + range(0, s.num_nodes):
        
        #node = c.nodes[node]
                
        print '// {0}'.format(node)
        node_name = '"{0}" [ shape="record"'
        if node != 'X':
            node_name += ' label="{0}|<L> L | <R> R"'
        node_name += '];'
        print node_name.format(node)
        
        if node != 'X':
            edge_l = str(node)+'L'
            print '"{0}":L:s -> {1}:n [color="red"];'.format(node, print_viz(s.to[edge_l]))
            edge_r = str(node)+'R'
            print '"{0}":R:s -> {1}:n [color="green"];'.format(node, print_viz(s.to[edge_r]))
        else:
            print '"{0}":s -> {1}:n;'.format(node, print_viz(s.to[node]))

        print " "
    
    print "}"
    

if __name__ == '__main__':
    main()
    