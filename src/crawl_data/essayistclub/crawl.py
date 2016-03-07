from bs4 import BeautifulSoup
import urllib

base = "http://www.essayistclub.or.kr/"

for i in range(1,100):
	for j in range(1,10):
		if(i<10):
			r = urllib.urlopen(base + '0' + str(i) + 'm' + '0' + str(j) + '.htm').read()
		else:
			r = urllib.urlopen(base + str(i) + 'm' + '0' + str(j) + '.htm').read()
		b = BeautifulSoup(r)
    		if '404' in b.find('title').text:
    			break
    		else:
    			text = BeautifulSoup(r).find('table').text
			print text