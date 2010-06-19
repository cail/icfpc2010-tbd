from circuit_viz import *
import sys

def main():

    f = file(sys.argv[1])
    
    c = Circuit(f.read())
    
    print "<TOUCHGRAPH_LB >"
    
    print "<NODESET >"
        
    for node in sorted(c.nodes.keys()):
        node = c.nodes[node]
                
        node_name = '<NODE nodeID="node{0}"> <NODE_LABEL label="{0}" fontSize="14" textColor="#ffffff"/>'
        if node.name == 'X':
            node_name += ' <NODE_LOCATION visible="true"/> '
        node_name += '</NODE>'
        print node_name.format(node.name)
    print "</NODESET >"
    print "<EDGESET >"
        
    for node in sorted(c.nodes.keys()):
        node = c.nodes[node]
        if node.name != 'X':
            print '<EDGE fromID="node{0}" toID="node{1}" type="1" color="#FF0000" visible="true"/>'.format(node.name, node.nout[0][0])
            print '<EDGE fromID="node{0}" toID="node{1}" type="1" color="#00FF00" visible="true"/>'.format(node.name, node.nout[1][0])
        else:
            print '<EDGE fromID="node{0}" toID="node{1}" type="1" color="#000000" visible="true"/>'.format(node.name, node.nout[0][0])
        
    print "</EDGESET >"
    print "</TOUCHGRAPH_LB >"
    

if __name__ == '__main__':
    main()
