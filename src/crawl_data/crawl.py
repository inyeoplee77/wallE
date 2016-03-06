from bs4 import BeautifulSoup
import urllib

f = open("data_supil","w")
number = 51438
for i in range(51438,0,-1):
	
	r = urllib.urlopen("http://www.supil.or.kr/essay/talkbox/viewbody.html?partid=29&code=talkbox2&page=1&number="+str(i)+"&keyfield=&key=").read()	
	text = BeautifulSoup(r).select('td[bgcolor="#FFFFFF"]')
	if len(text) < 1:
		continue
	text = text[1].text
	if not text:
		continue
	f.write(text.encode('utf-8'))

