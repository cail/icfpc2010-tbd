import re
import mechanize
import sys
import time
import csv
from submit_fuel import login
from submit_car import PASSWD, USER
from mechanize._beautifulsoup import BeautifulSoup, BeautifulStoneSoup

def refresh_ids(br=None):
    
    br = mechanize.Browser()
    
    data = csv.reader(open('../data/car_ids'))
    data = list(data)
    
    newcars = []
    maxid = 0
    oldmaxid = 0
    
    for c in data:
        if len(c) < 2:
            continue
        if int(c[0]) > maxid:
            maxid = int(c[0])
    print maxid
    
    while(oldmaxid != maxid):
        print "request ", maxid 
        response = br.open("http://nfa.imn.htwk-leipzig.de/recent_cars/?G0="+str(maxid))
        oldmaxid = maxid
        
        body = response.read()
        #body = open('body').read()
        #print body
        bs = BeautifulSoup(body)
    
        for pre in bs.fetch('pre'):
            vdata = pre.renderContents()
            m = re.match(r"\((\d+),.*?\&quot\;([012]+)\&quot\;\)", vdata)
            data = ()
            if m:
                data = (m.group(1), m.group(2))
                newcars.append( data )
                if data[0] > maxid:
                    maxid = data[0]
        
    cid = open('../data/car_ids', 'a')
    cdata =open('../data/car_data', 'a')
    for c in newcars:
        cid.write("{0}, 0\n".format(c[0]))
        cdata.write("{0}, {1}\n".format(c[0], c[1]))
        
    return newcars
        
if __name__ == '__main__':
    
    refresh_ids()
