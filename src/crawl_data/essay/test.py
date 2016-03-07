from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen("http://www.qtessay.or.kr/n23a200.htm").read()
if '404' in BeautifulSoup(r).find('title').text:
	print 'asd'

