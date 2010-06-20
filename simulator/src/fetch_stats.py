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
    
if __name__ == '__main__':
    
    (score, csolved, csubmitted) = fetch_stats()
    
    print "Score: ", score
    print "Solved: ", csolved
    print "Submitted: ", csubmitted
