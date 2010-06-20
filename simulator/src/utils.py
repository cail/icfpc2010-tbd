# for uncategorized garbage

def dict_id(domain):
    return dict((x, x) for x in domain)

def dict_compose(a, b):
    return dict((x, b[a[x]]) for x in a)