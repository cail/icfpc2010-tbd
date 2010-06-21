import mechanize
import sys
import time
from submit_car import PASSWD, USER
from mechanize._beautifulsoup import BeautifulSoup

# this function is not meant to be called by anyone.
#def transition_to_part_2():
#    br = mechanize.Browser()
#
#    def fetch_all_ids():
#        with open('ids.new', 'w') as f:
#            print 'fetching all the shit'
#            for i in range(200):
#                print 'page%d' % i
#                response = br.open("http://icfpcontest.org/icfp10/score/instanceTeamCount?page=%d&size=10" % i)
#                assert br.viewing_html()
#                body = response.read()
#                bs = BeautifulSoup(body)
#                ids = []
#                for tr in bs.fetch('tr'):
#                    for td in tr.fetch('td'):
#                        if (td.get('style') or '').strip() == 'width: 20%;': 
#                            ids.append(td.contents[0])
#                if not ids: break
#                f.write(', 0\n'.join(ids) + '\n')
#                f.flush()
#                time.sleep(0.5)
#            print 'done'
#
#    def leave_only_new_ids():
#        total_ids = set()
#        old_ids = set()
#        with open('ids.new', 'r') as f:
#            for s in f:
#                s = s.strip()
#                if not s: continue
#                id = s.split(',')[0].strip()
#                total_ids.add(id)
#        print 'Total ids:', len(total_ids)
#        
#        with open('../data/car_ids', 'r') as f:
#            for s in f:
#                s = s.strip()
#                if not s: continue
#                id = s.split(',')[0].strip()
#                old_ids.add(id)
#        print 'Old ids:', len(old_ids)
#
#        new_ids = total_ids - old_ids
#        print 'New ids:', len(new_ids)
#        new_ids = reversed(sorted([int(id) for id in new_ids]))
#        with open('car_ids', 'w') as f:
#            for id in new_ids:
#                print >>f, '%d, 0' % id
#        print 'yay'



CAR_DATA_FILE = '../data/car_data'
CAR_IDS_FILE = '../data/car_ids'

def login():
    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    assert br.viewing_html()
    
    br.select_form(name="f")    
    br["j_username"] = USER
    br["j_password"] = PASSWD
    br.submit()
    return br

def get_car_data(br, id):
    for _ in range(2):
        try:
            res = br.open("http://icfpcontest.org/icfp10/instance/{0}/solve/form".format(id))
            body = res.read()
            bs = BeautifulSoup(body)
            form = bs.fetch('form')[0]
            data = form.div.contents[1]
            return data
        except Exception as exc:
            print 'Omg! ' + str(exc)
        

def update_car_data(br, ids):
    with open(CAR_DATA_FILE, 'r') as f:
        existing_ids = set(filter(None, (s.strip() for line in f.readlines() for s in line.split(','))))
    new_ids = ids - existing_ids
    total_len = len(ids)
    new_len = len(new_ids)
    print 'total/new/rejected ids:', total_len, new_len, total_len - new_len 
    
    if new_ids:
        with open(CAR_DATA_FILE, 'a') as f:
            for i, id in enumerate(new_ids):
                cardata = get_car_data(br, id)
                print>>f, "%s, %s" % (id, cardata)
                f.flush()
                print '%d/%d' % (i + 1, new_len)
                time.sleep(0.2)

def update_ids(ids, level):
    print 'updating car_ids'
    with open(CAR_IDS_FILE, 'a') as f:
        for id in ids:
            print>>f, '%s, %d' % (id, level) 
        
            
def load_ids():
    print 'loading old ids'
    ids = set()
    max_level = 0
    with open(CAR_IDS_FILE, 'r') as f:
        for s in f:
            s = s.strip()
            if not s: continue
            id, level = map(int, s.split(','))
            ids.add(str(id))
            max_level = max(level, max_level)
    return ids, max_level

def fetch_new_ids(br, old_ids):
    print 'fetching new ids'
    new_ids = set()
    for i in range(200):
        print 'page%d' % i
        response = br.open("http://icfpcontest.org/icfp10/score/instanceTeamCount?page=%d&size=10" % i)
        assert br.viewing_html()
        body = response.read()
        bs = BeautifulSoup(body)
        page_ids = set()
        for tr in bs.fetch('tr'):
            for td in tr.fetch('td'):
                if (td.get('style') or '').strip() == 'width: 20%;': 
                    page_ids.add(td.contents[0].strip())
        if not page_ids: break
        old_page_ids = page_ids & old_ids
        page_ids -= old_page_ids
        new_ids.update(page_ids)
        if old_page_ids: break # if we see any old ids
        time.sleep(0.5)
    print '%d new ids fetched' % len(new_ids)
    return new_ids

def update():
    br = login()
    ids, max_level = load_ids()
    new_ids = fetch_new_ids(br, ids)
    update_car_data(br, new_ids)
    max_level += 1
    print 'NEW LEVEL: ', max_level 
    update_ids(new_ids, max_level)
    print 'Done. AND AGAIN! %d new ids created with level = %d!' % (len(new_ids), max_level)

if __name__ == '__main__':
    update()