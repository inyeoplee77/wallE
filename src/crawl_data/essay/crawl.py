from bs4 import BeautifulSoup
import urllib

base = "http://essay.or.kr/gnu4/bbs/board.php"
essay = "?bo_table=essay100"
oversea = "?bo_table=overseasessay"
#&page=2
def crawl_text(url,p):
	for i in range(1,p):
		r = urllib.urlopen(base+url+str(i)).read()
		tds = BeautifulSoup(r).select('td[style="word-break:break-all;"]')
		for td in tds:
			r = urllib.urlopen(base.split('bbs')[0] + td.find('a')['href'][3:]).read()
			text = BeautifulSoup(r).find('span','ct lh')
			if not text:
				continue
			text = text.text
			print text
#essay100
crawl_text(essay + "&page=",7)
#oversea
crawl_text(oversea + "&page=",5)
