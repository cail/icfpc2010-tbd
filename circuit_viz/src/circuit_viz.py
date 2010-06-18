import re
import sys

def parse_target(t):
    if t == 'X':
        return ('X')
    return (t[:-1], t[-1:])

def print_target(t):
    if len(t) == 1:
        return t[0]
    return '"'+t[0]+'":'+t[1]

    
def main():

    f = file(sys.argv[1])
    
    lines = f.readlines()
    nodes_count = int( lines[0].strip()[0:-2] ) + 2
    
    print "digraph unix {"
    print ' rank=sink; weight=1;  '
    for node_no in range(0, int(nodes_count)):
        
        line = lines[node_no].strip()
        
        if node_no == 0:
            node = line[:-1]
            out = parse_target(node)
            print '"X" [ shape="record" ];'
            print '"{0}" -> {1};'.format('X', print_target(out))
            continue
        
        node = line[:-1]
        (node_in, node_out) = node.split('#')
        node_in = node_in[:-1]
        #print win
        #print wout
        
        match = re.match(r"(\d+[LR]|X)(\d+[LR]|X)", node_in)
        if match:
            node_in_left = parse_target( match.group(1) )
            node_in_right = parse_target( match.group(2) )
        match = re.match(r"(\d+[LR]|X)(\d+[LR]|X)", node_out)
        if match:
            node_out_left = parse_target( match.group(1) )
            node_out_right = parse_target( match.group(2) )
        
        print '// {0}'.format(node)
        node_no = node_no-1
        print '"{0}" [ shape="record" label="{0}|<L> L | <R> R"];'.format(node_no)
        
        #print '"{0}":{2} -> "{1}":L;'.format(win_left[:-1],  node_no, win_left[-1:])
        #print '"{0}":{2} -> "{1}":R;'.format(win_right[:-1], node_no, win_right[-1:])

        print '"{0}":L:s -> {1}:n;'.format(node_no, print_target(node_out_left))
        print '"{0}":R:s -> {1}:n;'.format(node_no, print_target(node_out_right))

        print " "
        
    
    print "}"
    

if __name__ == '__main__':
    main()
    