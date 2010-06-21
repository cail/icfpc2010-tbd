import sys
sys.path.append('../../simulator/src')

from time import time
from collections import namedtuple
from os import path as os_path
from copy import copy
from pprint import pformat
import traceback
from functools import wraps

from submit_fuel import list_cars 
from utils import rename_file
from StringIO import StringIO
from itertools import islice

#################

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


def create_rpc_server(instance):
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    server = SimpleXMLRPCServer(("127.0.0.1", 8333),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_function(lambda req: 'ACQ "' + req + '"', 'server_test')
    server.register_instance(instance)
    return server


#################


class ServerException(Exception):
    def __init__(self):
        msg = traceback.format_exc()
        Exception.__init__(self, msg)

def server_method(f):
    name = f.__name__
    @wraps(f)
    def wrapper(*args, **kwargs):
        print '%s: begin' % name
        try:
            res = f(*args, **kwargs)
            print '%s: end' % name
            return res
        except Exception:
            exc = ServerException()
            print '%s: exception: %s' % (name, str(exc))
            raise exc
    wrapper.original_function = f
    return wrapper

CACHE_FILE = 'sync_server_data.txt'
TMP_FILE = 'sync_server_data.tmp'
BACKUP_FILE = 'sync_server_data.bak'
SAVE_INTERVAL = 60.0

class Car_info(object):
    __slots__ = 'id suppliers source'.split()
    
    def __init__(self, id, **kwargs):
        set = object.__setattr__
        for k in self.__slots__:
            set(self, k, None)
        set(self, 'id', id)
        for k, v in kwargs.iteritems():
            set(self, k, v)

    def __repr__(self):
        return ('Car_info(' + 
                ', '.join(k + '=' + repr(getattr(self, k)) for k in self.__slots__) +
                ')')
    def __setattr__(self, key, value):
        raise Exception('Immutable, motherfucker, which letter do you not understand?')
    
    def update(self, **kwargs):
        """Ignores None arguments"""
        new = dict((k, getattr(self, k, None)) for k in self.__slots__) 
        for k, v in kwargs.iteritems():
            if v is None: continue
            new[k] = v
        return Car_info(new)


def newest_file(*names):
    def ftime(name):
        if os_path.exists(name):
            return os_path.getmtime(name), name
        else:
            return 0.0, None
    return max(map(ftime, names))[1]

class Sync_server(object):
    def _update_car_ids(self):
        self.ids = dict((car.id, i) for i, car in enumerate(self.cars))
        
    def __init__(self):
        fname = newest_file(CACHE_FILE, TMP_FILE, BACKUP_FILE)
        if fname:
            with open(fname, 'r') as f:
                self.cars = eval(f.read())
        else:
            self.cars = []
        self._update_car_ids()
        self.last_save = time()
        self.dirty = False
        
    def _get_car(self, id):
        pos = self._ids(
        return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end        car = self.cars.get(id, None)
        if car is None:
            car = Car_info(id)
        return car
    
    @server_method
    def update_cars(self, lst):
        new = []
        for data in lst:
            new.append(self._get_car(id).update(data))
        self.cars.extend(new)
        self.cars.sort()
        self.dirty = True
            
            
    @server_method
    def select_cars(self, limit = 100, full = False, specific_ids = None, has_source = None):
        """
        limit 
        """
        def strip_car_info(car):
            source = '' if car.source is not None else None
            return car.update(source=source)
        if full: strip_car_info = lambda x: x
        res = {}
        for car in self.cars:
            id = car.id
            if has_source is not None and (car.source is not None) != has_source: continue
            if specific_ids is not None and car.id
            
            res[id] = strip_car_info(car)
            if len(res) >= limit: break
        return res
    
    def _prepare_dump(self):
        dump = StringIO() 
        dump.write('# car data\n')
        dump.write('{\n')
        for item in self.cars.iteritems():
            dump.write('  %r:%r,\n' % item)
        dump.write('}\n')
        return dump
    
    def _save_if_dirty(self, dump = None):
        if not self.dirty or time() - self.last_save < SAVE_INTERVAL:
            return 'No changes detected'
        
        if dump is None: dump = self._prepare_dump()

        if os_path.exists(TMP_FILE):
            rename_file(TMP_FILE, BACKUP_FILE)
        with open(TMP_FILE, 'w') as f:
            f.write(dump)
        res = 'Data saved to: "' + os_path.realpath(TMP_FILE) + '"'
        print res
        return res
    
    @server_method
    def commit(self):
        dump = self._prepare_dump()
        self._save_if_dirty(dump)
        with open(CACHE_FILE, 'w') as f:
            f.write(dump)
        res = 'Data committed to: "' + os_path.realpath(CACHE_FILE) + '"'
        print res
        return res

if __name__ == '__main__':
    sync_server = Sync_server()
    rpc_server = create_rpc_server(sync_server)
    print 'running'
    # Run the server's main loop
    while True:
        try:
            rpc_server.serve_forever()
        except KeyboardInterrupt:
            # that's no good at all actually!
            print 'KeyboardInterrupt!'
            # rpc_server.shutdown()
            sync_server._save_if_dirty()
            break;
    print 'done'
