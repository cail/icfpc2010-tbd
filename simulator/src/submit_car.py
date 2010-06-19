import re
import mechanize
import sys

def submit_car(vehicle, fuel):

    br = mechanize.Browser()
    br.open("http://icfpcontest.org/icfp10/login")
    # follow second link with element text matching regular expression
    
    assert br.viewing_html()
    
    print br.title()
    
    br.select_form(name="f")
    
    br["j_username"] = "TBD"
    br["j_password"] = "460291662043320768111588216149264970701887731096381490177520"
    
    response = br.submit()
    
    print response.geturl()
    
    response = br.follow_link(text_regex=r".* new car.*")
    
    br.select_form(nr=0)
        
    br["problem"] = vehicle
    br["exampleSolution.contents"] = fuel
    
    response = br.submit()
    
    #print response.info()  # headers
    body =  response.read()  # body
    
    re_err = re.compile(r".*\<pre\>(.*)\</pre\>", re.S+re.M)
    m = re_err.match(body)
    
    if m:
        error = m.group(1)
        return error
        
    else:
        print "ok!"
    
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "use <vehiclefile> <fuelfile>"
         
    else:
        vehicle = sys.argv[1]
        
        if re.match(r"[012]+", vehicle):
            pass
        else:
            vehicle = open(vehicle).read()

        fuel = open(sys.argv[2]).read()
        
        result = submit_car(vehicle, fuel)
        
        print result
    