from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen("http://www.supil.or.kr/essay/talkbox/viewbody.html?partid=29&code=talkbox2&page=1&number=51438&keyfield=&key=").read()

number = 51438
soup = BeautifulSoup(r).select('td[bgcolor="#FFFFFF"]')[1]

print soup
