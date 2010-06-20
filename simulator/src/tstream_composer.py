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
    
def compose_list(lst, composer, sort_items = False):
    """sort_items is a kind of hack that is only used in compose_chambers to 
    produce the lexicographically smallest car representation.
    Important note: this IS NOT enough to normalize a car, because the 
    equivalence relations allows permuting tanks and that should be done
    externally. 
    """ 
    length = len(lst)
    if   length == 0: return '0'
    elif length == 1: return '1' + composer(lst[0])
    else:
        items = [composer(i) for i in lst]
        if sort_items: items.sort()
        return ('22' + 
                compose_number(length - 2) + 
                ''.join(items))

# fuel
def compose_row(row):
    return compose_list(row, compose_number)

def compose_matrix(matrix):
    return compose_list(matrix, compose_row)
    
def compose_matrices(matrices):
    return compose_list(matrices, compose_matrix)

# car
def compose_type(t):
    assert t in [0, 1]
    return compose_number(t)
    
def compose_chamber(chamber):
    assert len(chamber) == 3
    l1 = compose_list(chamber[1], compose_number)
    t  = compose_type(chamber[0])
    l2 = compose_list(chamber[2], compose_number)
    return l1 + t + l2

def compose_chambers(chambers):
    return compose_list(chambers, compose_chamber, sort_items = True)
