from bs4 import BeautifulSoup
import urllib

#f = open("data_djhpoem","w")
#number = 51438
base = "http://djhpoem.co.kr"
#/board/?c=3_product/3_5


def crawl_text(url,p):
	for i in range(1,p):
		r = urllib.urlopen(base+url+str(i)).read()	
		tds = BeautifulSoup(r).find_all('td', "sbj")
		for td in tds:
			r = urllib.urlopen(base + td.find('a')['href']).read()
			text = BeautifulSoup(r).select('div#vContent')
			if not text:
				continue	
			text = BeautifulSoup(r).select('div#vContent')[0].text

#poem
crawl_text("/board/?c=3_product/3_5&p=",23)

crawl_text("/board/?c=3_product/3_2&p=",10)
#/board/?c=3_product/3_2&p=

