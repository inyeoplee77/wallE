from bs4 import BeautifulSoup
import urllib

#f = open("data_djhpoem","w")
base = "http://djhpoem.co.kr"

board = "/board/?c=3_product/"

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
crawl_text(board + "3_5&p=",23)
#prose
crawl_text(board + "3_2&p=",10)
#sing
crawl_text(board + "3_4&p=",5)
#
crawl_text("/board/?c=5_letter/5_1&p=",14)
#letter from poet
crawl_text("/board/?c=5_letter/5_2&p=",20)


