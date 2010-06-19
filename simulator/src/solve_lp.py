
from pulp import *

def solve_LP(car):
    # since we are in logspace, all variables should be strictly positive
    
    eps = 1
    vars = [LpVariable('x%d'%i, lowBound=eps, cat=LpInteger) 
            for i in range(car.num_tanks)]
    problem = LpProblem('search for fuel', LpMinimize)
    problem += lpSum(vars)
    
    for chamber, isMain in car.all_chambers():
        coeffs = [0]*car.num_tanks
        for i in chamber.upper:
            coeffs[i] += 1
        for i in chamber.lower:
            coeffs[i] -= 1
        # i'm not doing it as difference of lpSums because it's buggy
        term = lpSum(coeff*var for coeff, var in zip(coeffs, vars))
        assert len(term) != 0, 'pipes are equivalent'
        if isMain:
            problem += term >= eps
        else:
            problem += term >= 0
    
    result = problem.solve_cnf(GLPK(msg=False))
    
    if result != LpStatusOptimal:
        print problem
        result = problem.solve_cnf(GLPK(msg=True))
        print LpStatus[result]
        assert False
    
    # go back from logspace to linear space
    return [2**value(v) for v in vars]
