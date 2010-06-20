import psyco
psyco.full()

from time import clock
from itertools import *
from collections import defaultdict

from utils import *
from scheme import *

# attempt to find interesting schemes
# constants and something like that

def find_constants(num_blocks):
    n = 0
    for from_ in permutations(range(2*num_blocks+1)):
        n += 1
        if n%1000 == 0:
            print n
        #print 'testing', from_
        back_edges = 0
        for to,fr in enumerate(from_):
            if to == 0 or fr == 0:
                continue # input or output can't be back edge
            if (to-1)//2 <= (fr-1)//2:
                back_edges += 1
        # 3**back_edges is upper bound for number of scheme states
        constant = True
        result = None
        for inputs in product(range(3), repeat=3**back_edges):
            if result is None:
                result = eval_scheme(from_, inputs)
            else:
                if not eval_scheme_and_compare(from_, inputs, result):
                    constant = False
                    break
        if constant:
            print 'found constant', from_
            print 'with output', eval_scheme(from_, [0]*10)


def linear_sequences(num_gates):
    if num_gates == 0:
        return set([()])
    
    generated = set()
    for ins in linear_sequences(num_gates-1):
        for cross in [False, True]:
            outs = []
            for left_in, right_in in ((0,0),)+ins:
                if cross:
                    left_in, right_in = right_in, left_in
                outs.append(gate_function(0,left_in,right_in))
            outs = tuple(outs)
            generated.add(outs)
    return generated


trit_pairs = [(i,j) for i in range(3) for j in range(3)]

cross_dict = dict(((i,j),(j,i)) for i,j in trit_pairs)

class SequenceTree(object):
    @staticmethod
    def root(num_gates):
        root = SequenceTree()
        root.num_gates = num_gates
        root.parent = None
        root.cross = None
        root.function = dict_id(trit_pairs)
        root.output = (0,0)
        return root
        
    def subtrees(self):
        child = SequenceTree()
        child.num_gates = self.num_gates
        child.parent = self
        child.cross = False
        child.function = dict_compose(gate_dict, self.function)
        child.output = child.function[(0,0)]
        yield child
        child = SequenceTree()
        child.parent = self
        child.cross = True
        child.function = dict_compose(dict_compose(gate_dict, cross_dict), self.function)
        child.output = child.function[(0,0)]
        yield child
        
    def get_outputs(self):
        outputs = []
        node = self
        while node is not None:
            outputs.append(node.output)
            node = node.parent
        outputs.reverse()
        return outputs

def rec(deep, node):
    print node.get_outputs()
    if deep == 0:
        return
    for child in node.subtrees():
        rec(deep-1, child)



if __name__ == '__main__':
    rec(2, SequenceTree.root())
    #find_constants(4)
    print 'done'