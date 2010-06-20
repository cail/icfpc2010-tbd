# for uncategorized garbage
import os
from os import path as os_path

def dict_id(domain):
    return dict((x, x) for x in domain)

def dict_compose(a, b):
    return dict((x, b[a[x]]) for x in a)

def rename_file(oldname, newname):
    if os.name == 'nt' and os_path.exists(oldname):
        try:
            os.remove(newname)
        except OSError, exc:
            import errno
            if exc.errno != errno.ENOENT: raise exc
    os.rename(oldname, newname)
