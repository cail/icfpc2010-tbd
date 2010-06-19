import re
import mechanize
import sys
from submit_car import PASSWD, USER
from mechanize._beautifulsoup import BeautifulSoup, BeautifulStoneSoup

def submit_fuel(vehicle, fuel):

    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    assert br.viewing_html()
    #print br.title()
    
    br.select_form(name="f")
    
    br["j_username"] = USER
    br["j_password"] = PASSWD
    
    response = br.submit()
    
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
    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    assert br.viewing_html()
    
    br.select_form(name="f")    
    br["j_username"] = USER
    br["j_password"] = PASSWD
    response = br.submit()
        
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
        
        
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "use <vehicleid> <fuelfile or ->"
        print "or listcars"
         
    else:
        if len(sys.argv) == 2 and sys.argv[1] == 'listcars':
            list =  list_cars()
            for item in list:
                print "{0}, {1}".format(item[0], item[1])

        else:
            vehicle = sys.argv[1]
            fuel = sys.argv[2]
            
            fuel = open(fuel).read()
            
            result = submit_fuel(vehicle, fuel)
            
            print
            print result
            print 
