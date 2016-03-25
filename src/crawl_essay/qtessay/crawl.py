from bs4 import BeautifulSoup
import urllib

f = open("test1.txt", "w")


for i in range(1, 10):
	for j in range (1, 10):
		r = urllib.urlopen("http://www.qtessay.or.kr/n"+str(0)+str(i)+"a"+str(0)+str(j)+".htm").read()
		text = BeautifulSoup(r).find('table').text
		print text
for i in range(10, 73):
	for j in range (10, 50):
		r = urllib.urlopen("http://www.qtessay.or.kr/n"+str(i)+"a"+str(j)+".htm").read()
		b = BeautifulSoup(r)
    	if '404' in b.find('title').text:
      		break
    	text = b.find('table').text
    	if len(text)<1:
    		continue
    	else:
    		print text

