import xmlrpclib
import threading
import time
import os.path as os_path
from ConfigParser import SafeConfigParser

CONFIG_PATH = '.sync.ini'
SECTION = 'sync'

def Sync_client():
    parser = SafeConfigParser()
    parser.read(CONFIG_PATH)
    conf_modified = False
    if not parser.has_option(SECTION, 'address'):
        address = raw_input('Specify sync server address (for example, "http://localhost:8333"): ')
        conf_modified = True
    else:
        address = parser.get(SECTION, 'address')
   
    s = xmlrpclib.ServerProxy(address)
    
    print 'Sync test response:', s.server_test('REQ')
    if conf_modified:
        if not parser.has_section(SECTION): parser.add_section(SECTION)
        parser.set(SECTION, 'address', address)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)
    return s
         
if __name__ == '__main__':
    s = Sync_client()
    print s.system.listMethods()
    print s.select_cars()
    

