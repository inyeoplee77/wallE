from bs4 import BeautifulSoup
import urllib

#f = open("data_djhpoem","w")
#number = 51438
base = "http://djhpoem.co.kr"
#/board/?c=3_product/3_5

for p in range(1,23):
	r = urllib.urlopen(base+ "/board/?c=3_product/3_5&p="+str(p)).read()	
	tds = BeautifulSoup(r).find_all('td', "sbj")
	for td in tds:
		r = urllib.urlopen(base + td.find('a')['href']).read()
		text = BeautifulSoup(r).select('div#vContent')[0].text
