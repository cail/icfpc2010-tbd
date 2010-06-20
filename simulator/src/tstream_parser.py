import inspect

def decode_base3(lst):
    acc = 0
    for i in lst:
        acc = acc * 3 + i
    return acc

def get_char(stream):
    return stream.next()

def get_char_debug(stream):
    caller = inspect.stack()[1][3]
    print caller + ':',
    c = stream.next()  
    print c
    return c

# uncomment or execute somewhere else this for debugging:
#get_char = get_char_debug

def parse_digit(stream):
    c = get_char(stream)
    return int(c)

def parse_number(stream):
    lst = parse_list(stream, parse_digit)
    n = decode_base3(lst)
    p = sum(3**i for i in range(len(lst)))
    return p + n
    
def parse_list(stream, parser):
    c = get_char(stream)
    if   c == '0': return []
    elif c == '1': return [parser(stream)]
    elif c == '2':
        assert get_char(stream) == '2'
        length = parse_number(stream) + 2
        return [parser(stream) for _ in range(length)]
    assert False, c

# cars
    
def parse_type(stream):
    t = parse_number(stream)
    assert t in [0, 1]
    return t 
    
def parse_chamber(stream):
    l1 = parse_list(stream, parse_number)
    t  = parse_type(stream)
    l2 = parse_list(stream, parse_number)
    return (t, l1, l2)

def parse_end(stream):
    try:
        c = get_char(stream)
    except StopIteration:
        return
    assert False, 'Leftovers: ' + (c + ''.join(stream))

def parse_chambers(stream):
    chambers = parse_list(stream, parse_chamber)
    parse_end(stream)
    return chambers

# fuels

def parse_row(stream):
    return parse_list(stream, parse_number)

def parse_matrix(stream):
    return parse_list(stream, parse_row)

def parse_matrices(stream):
    res = parse_list(stream, parse_matrix)
    parse_end(stream)
    return res