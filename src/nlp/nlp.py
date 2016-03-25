# -*- coding: utf-8 -*-
from konlpy.tag import Twitter
import re
import os
import shutil


target = "../../nlp/data/"
base = '../../facebook/data/'
twitter = Twitter()
if not os.path.exists(base):
	if not os.path.exists(base[:-1] + '.tar.gz'):
		print 'no data'
		exit(1)
	else:
		print 'extracting data...'
		tarfile.open(base[:-1] + '.tar.gz','r').extractall(base)
		print 'extracting completed'

if not os.path.exists(target):
	os.mkdir(target)

y = raw_input( 'press y to clear data:')
if y == 'y':
	shutil.rmtree(target)
	os.mkdir(target)	


nonkorean = re.compile(u'[^ 가-힣]+',re.UNICODE)
nomean = re.compile(u'[ㄱ-ㅎ]|[가-힣\S]*대숲|[가-힣\S]*대나무숲|[0-9\S]*번째|[가-힣\S]*학교|#[가-힣\w0-9\S]+',re.UNICODE)

#nomean = re.compile(u'[가-힣\S]*대숲|[가-힣\S]*대나무숲|[0-9\S]*번째|[가-힣\S]*학교',re.UNICODE)
stopwords = [u'외대',u'한양대',u'고대', u'연대',u'중앙대',u'경북대',u'경희대',u'서울대',u'설대',u'성대',u'성균관대',u'서강대',u'서울시립대',u'댓글',u'시립대',u'서울시립대',u'오전',u'오후',u'외침',u'제보',u'숲',u'대숲',u'대나무숲',u'연대숲',u'서강대숲',u'이야기',u'대나무',u'설시대',u'오전',u'오후']

'''
text = open('203051796562493_257140657820273','r').read().decode('utf8')
for i in twitter.pos(text,norm=True,stem=True):
'''

for dir in os.listdir(base):	
	if os.path.isdir(base + dir):
		os.mkdir(target + dir)
		for file in os.listdir(base + dir):
			text = open(base+dir+'/'+file,'r').read().decode('utf8')
			f = open(target + dir + '/' + file,'w')
			text = nonkorean.sub('',nomean.sub(u' ',text))
			for i in twitter.pos(text,norm=True,stem=True):
				if i[1] != "Josa" and i[0] not in stopwords and len(i[0]) > 1:
					f.write(i[0].encode('utf8') + ' ')
			f.flush()
		print dir+ ' done'

print 'compressing data'
shutil.make_archive(target, 'gztar', target)
print 'compression completed'
