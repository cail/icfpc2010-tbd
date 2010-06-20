import sys

def encode_base3(n, digits):
    acc = []
    for _ in range(digits):
        n, m = divmod(n, 3)
        acc.append(m)
    assert n == 0          
    acc.reverse()
    return acc

def compose_digit(n):
    assert n in [0, 1, 2]
    return str(n)

def compose_number(n):
    p = 0
    for i in xrange(10000):
        p_prev = p
        p += 3 ** i
        if n < p:
            digits = encode_base3(n - p_prev, i)
            return compose_list(digits, compose_digit)
    # wtf?
    assert False
    
def compose_list_many(lst, composer):
    length = len(lst)
    assert length >= 2
    return ('2' +
            compose_number(length - 2) + 
            ''.join(composer(i) for i in lst))

def compose_list(lst, composer):
    length = len(lst)
    if   length == 0: return '0'
    elif length == 1: return '1' + composer(lst[0])
    else:             return '2' + compose_list_many(lst, composer)

def compose_row(row):
    return compose_list(row, compose_number)

def compose_matrix(matrix):
    return compose_list(matrix, compose_row)
    
def compose_matrices(matrices):
    return compose_list(matrices, compose_matrix)
