import os
from pprint import pprint


def solve_cnf(cnf):
    """
    Accept list of clauses.
    
    For instance  (x1) and (not x1 or x2)
    is [[1],[-1,2]]
    
    Return pair (isSatisfiable, variables)
    
    If formula is satisfiable, variables corresponding truth assignment.
    For instance, for x1=1, x2=0
    it's [1,-2]
    """
    
    inputFileName = "sat_input.txt"
    outputFileName = "sat_output.txt"
    logFileName = "sat_log.txt"
    
    with open(inputFileName,"w") as input:
        for clause in cnf:
            print>>input, " ".join(map(str,clause)), 0

    os.system("minisat %s %s >%s"%(inputFileName, outputFileName, logFileName))
    
    with open(outputFileName) as output:
        result = output.readline().strip()
        result = {'SAT': True, 'UNSAT': False}[result]
        variables = None
        if result:
            variables = map(int, output.readline().split())
            assert variables[-1] == 0
            variables = variables[:-1]
    
    os.remove(inputFileName)
    os.remove(outputFileName)
    os.remove(logFileName)
    return result, variables


class CNFBuilder(object):
    def __init__(self):
        self.num_vars = 0
        self.clauses = []
        
        self.one = self.new_var()
        self.clauses.append([self.one])
        
    def new_var(self):
        self.num_vars += 1
        return self.num_vars
    
    def new_vars(self,n):
        for i in range(n):
            yield self.new_var()
            
    def add_constraint(self, constraint, *vars):
        if len(vars) == 0:
            self.clauses += constraint
            return
        
        tr = dict((sign*(i+1), sign*vars[i]) 
                  for i in range(len(vars)) for sign in [-1,1])
        for clause in constraint:
            self.clauses.append([tr[v] for v in clause])
            
            
    def solve(self):        
        self.satisfiable, variables = solve_cnf(self.clauses)
        self.values = {}
        if self.satisfiable:
            for v in variables:
                self.values[abs(v)] = 1 if v>0 else 0
            
    def value(self, *vars):
        result = 0
        for v in reversed(vars):
            result *= 2
            if v > 0:
                result += self.values[v]
            else:
                result += 1-self.values[-v]
        return result
    
    def print_solution(self):
        if not self.satisfiable:
            print 'UNSAT'
            return
        print 'SAT'
        for i in range(2, self.num_vars+1):
            print 'var%s = %s'%(i, self.values.get(i,'*'))
        


def bit2sign(x):
    return {0:-1, 1:1}[x]


        
if __name__ == '__main__':
    
    cnf = CNFBuilder()
    x, y, z = cnf.new_vars(3)
    
    
    cnf.add_constraint([[1,2],[-1],[2]], x, y)
    cnf.solve()
    
    cnf.print_solution()
    
