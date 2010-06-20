import re
import mechanize
import sys
import time
from submit_fuel import login
from submit_car import PASSWD, USER
from mechanize._beautifulsoup import BeautifulSoup, BeautifulStoneSoup

def fetch_stats(br=None):
    
    if br is None:
        br = login()
    
    response = br.open("http://icfpcontest.org/icfp10/")
    
    body = response.read()
    #body = open('body').read()
    #print body
    bs = BeautifulSoup(body)

    score = bs.fetch('div', {'id': '_score_id'})[0].renderContents()
    csolved = bs.fetch('div', {'id': '_solution_id'})[0].renderContents()
    csubmitted = bs.fetch('div', {'id': '_instance_id'})[0].renderContents()
    
    return (score, csolved, csubmitted)
    
def fetch_results():
    br = mechanize.Browser()
    response = br.open("http://icfpcontest.org/icfp10/score/teamAll")
    
    body = response.read()
    #body = open('body').read()
    #print body
    bs = BeautifulSoup(body)

    tbody = bs.fetch('table')
    
    if len(tbody) < 1:
        print "Server err"
        return None
    
    tds = tbody[0].fetch('td')

    results = []
    for i in range(0, len(tds)/2):
        if i < 2:
            continue
        val = tds[i*2].renderContents()
        name = tds[i*2+1].renderContents()
        if val == '0,000':
            continue
        if name == 'TBD':
            rank = i
        results.append(  (name, val) )

    return (rank, results)
    
    
if __name__ == '__main__':
    
    rank, results = fetch_results()
    print "Rank: ", rank
    
    (score, csolved, csubmitted) = fetch_stats()
    print "Score: ", score
    print "Solved: ", csolved
    print "Submitted: ", csubmitted
    
    for r in results:
        print r[0], " - ", r[1]
