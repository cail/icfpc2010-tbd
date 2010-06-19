import re
import mechanize
import sys

USER = "TBD"
PASSWD = "460291662043320768111588216149264970701887731096381490177520"

def submit_car(vehicle, fuel):

    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    # follow second link with element text matching regular expression
    
    assert br.viewing_html()
    
    #print br.title()
    
    br.select_form(name="f")
    
    br["j_username"] = USER
    br["j_password"] = PASSWD
    
    response = br.submit()
    
    #print response.geturl()
    
    response = br.follow_link(text_regex=r".* new car.*")
    
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
    
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "use <vehicledata/file> <fuelfile>"
         
    else:
        vehicle = sys.argv[1]
        fuel = sys.argv[2]
        
        if re.match(r"[012]+", fuel):
            vehicle, fuel = fuel, vehicle
        
        if re.match(r"[012]+", vehicle):
            pass
        else:
            vehicle = open(vehicle).read()

        fuel = open(fuel).read()
        
        result = submit_car(vehicle, fuel)
        
        print
        print result
        print 
    