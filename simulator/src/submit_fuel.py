import re
import mechanize
import sys
import time
from submit_car import PASSWD, USER
from mechanize._beautifulsoup import BeautifulSoup, BeautifulStoneSoup


def login():
    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    assert br.viewing_html()
    
    br.select_form(name="f")    
    br["j_username"] = USER
    br["j_password"] = PASSWD
    br.submit()
    return br

def submit_fuel(vehicle, fuel):

    br = login()
    
    response = br.open("http://icfpcontest.org/icfp10/instance/{0}/solve/form".format(vehicle))
    
    br.select_form(nr=0)
        
    br["problem"] = vehicle
    br["exampleSolution.contents"] = fuel
    
    response = br.submit()
    
    #print response.info()  # headers
    body =  response.read()  # body
#    print body
    
    re_spanerr = re.compile(r"class=\"errors\"\>(.*?)\<\/span\>", re.S+re.M)
    re_err = re.compile(r"\<pre\>(.*?)\</pre\>", re.S+re.M)

    m = re_err.search(body)
    mspan = re_spanerr.search(body)
    if mspan:
        error = mspan.group(1)
        return error
    elif m:
        error = m.group(1)
        return error
    else:
        return "OK " + body

def list_cars():

    br = login()
            
    response = br.follow_link(text_regex=r".*Submit fuel.*")
    body = response.read()
    
    #print body
    #body = open('body').read()
    
    bs = BeautifulSoup(body)
    #print bs.prettify()
    #print bs.nextSibling.prettify()
    ids = []
    for tr in bs.fetch('tr'):
        if len(tr.fetch('td')) < 1:
            continue
        suppliers = str(tr.fetch('td')[1].contents[0])
        
        f = tr.fetch('form')[0]
        id = f.get('action')
        m = re.search(r"\/(\d+)\/", id)
        id = m.group(1)
        
        ids.append( (id, suppliers))
    return ids
    
    
def get_cardata(br, car):
     
    if br == None:
        br = login()
    
    res = br.open("http://icfpcontest.org/icfp10/instance/{0}/solve/form".format(car))
     
    body = res.read()
     
    bs = BeautifulSoup(body)
    form = bs.fetch('form')[0]
    cardata = form.div.contents[1]
    return cardata
     
def load_cars():
    cars = open('data/car_ids').readlines()
    br = login()

    existing_cardata = open('data/car_data').readlines()

    allcardata = []
    
    for car in cars:
        c, no = car.split(', ')
        
        found = False
        for ec in existing_cardata:
            existingid = ec.split(', ') 
            if existingid[0] == c:
                sys.stderr.write("skipping {0}\n".format(c))
                found = True
        if found:
            continue
        sys.stderr.write("fetching '{0}' of {1}\n".format(c, len(cars)))
        cardata = get_cardata(br, c)
        allcardata.append( (c, cardata) )
        print "{0}, {1}".format(c, cardata)
        time.sleep(2)
    return
        
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "use <vehicleid> <fuelfile or ->"
        print "or listcars"
         
    else:
        if len(sys.argv) == 2:

            if sys.argv[1] == 'listcars':
                list =  list_cars()
                for item in list:
                    print "{0}, {1}".format(item[0], item[1])
    
            if sys.argv[1] == 'loadcars':
                load_cars()

        else:
            vehicle = sys.argv[1]
            fuel = sys.argv[2]
            
            fuel = open(fuel).read()
            
            result = submit_fuel(vehicle, fuel)
            
            print
            print result
            print 
