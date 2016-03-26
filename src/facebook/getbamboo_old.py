# -*- coding: utf-8 -*-
import requests
import os
import locale
import time
import shutil
appID = '719437504828313'
appSecret = 'dae1d765e81c02e566d6ccaa2b6af441'

token = "CAAKOUxjp05kBAGv2nl1XKZBWBp7bfyStp2FhRTzJTV3xJZBObadaYBSDyEEGDTezs81XofaYEbPtMdcBTwYHZCi99wHjuX6VWCNJesM6jEtF6UxhtqvHIidpGBm6u4pXnDuNFwpLjLl9HEqjJwIUI0ZBN4iJx57Tzu3qdoGZCuZB6LwdAf3816"

#token = "CAAKOUxjp05kBAMd0ihtkaLKrkjZAAZBkwUcSl1VOjdHypVyqgH4lIuaXjWfMdXNDgD4oEGA8FMMj8m2WjX9S9YmPOrbo67jypUki3eKtWln5wwGVMjvsb7mMLzAq8ZCTPYm7vkKm68uYJ9asTAb2JC77ntMnV8CATnGLAYLkZAjZA3nTzvOdfG4dOYMEf9LBs5C9uGYTNjwZDZD"

api = "https://graph.facebook.com/v2.5/"
para = {'access_token' : token}

f = open("../../data/facebook/bamboolist",'r')

pages = {}
for line in f:
	line = line.strip()
	line = line.split(',')
	pages[line[2]] = line[1]
posts = {}
page_errors = {}
likes_count = {}
likes_errors = {}
comments_errors = {}
comments_count = {}
who_likes_post = {}
who_comment_post = {}
share_count = {}
count = 0

#locale.setlocale(locale.LC_ALL,'')
#[^ ㄱ-ㅎ|ㅏ-ㅣㅣ가-힣]+
#nonkorean = re.compile(u'[^ 가-힣]+',re.UNICODE)
#hashtag = re.compile(u'#[가-힣\w0-9\S]+',re.UNICODE)
#nomean = re.compile(u'[ㄱ-ㅎ]|[가-힣\S]*대숲|[가-힣\S]*대나무숲|[0-9\S]*번째|[가-힣\S]*학교',re.UNICODE)
#print pages
from optparse import OptionParser

op = OptionParser()
op.add_option("--test",help="",dest="test",action='store_true',default=False)
op.add_option("--n-samples",type=int,default=100,dest="test_size",help="size of sample. default = 100")
op.print_help()
(opts, args) = op.parse_args()
if opts.test:
	print 'test mode... sample size = ' + str(opts.test_size) + 'per pages'
	dest = '../../data/facebook/test/data/'
else:
	dest = '../../data/facebook/data/'


time_count = 0
if not os.path.exists(dest):
	os.makedirs(dest)
else:
	y = raw_input('Would you like to clear data? (y/n)')
	if y =='y':
		shutil.rmtree(dest)
		os.makedirs(dest)
for page in pages:
	dir = pages[page].split('/')[-1]
	dir = dest + dir
	count = 0
	if not os.path.exists(dir):
		os.makedirs(dir)
	r = requests.get(api + page + "/posts",params = para).json()
	if 'error' in r:
		page_errors[page] = r['error']['message']
		if r['error']['code'] == 17:
			if time_count < 3:
				time.sleep(600)
				time_count += 1
		continue
	time_count = 0
	while 'previos' in r['paging']:
		r = requests.get(r['paging']['previous']).json()
	while True:
		if 'data' not in r:
			break
		for p in r['data']:
			f = open(dir+ '/' + p['id'],'w')
			if 'message' not in p:
				print 'message not in post'
				continue
			#message = nomean.sub(u' ',p['message'].strip())
			#message = u' '.join([voc for voc in nonkorean.sub(u'',hashtag.sub('',message)).split() if len(voc) < 10])			
			f.write(p['message'].encode('utf8')) #save as byte form
			count += 1
			try:
				share = requests.get(api+p['id'] + '?fields=shares',params=para).json()
				if 'shares' in share:
					share_count[p['id']] = share['shares']['count']#int
				else:
					share_count[p['id']] = 0
				
				likes = requests.get(api + p['id'] + '/likes?summary=true',params = para).json()
				if 'error' in likes:
					print 'likes error'
					likes_errors[p['id']] = likes['error']['message']
					if likes['error']['code'] == 17:
						if time_count < 3:
							time.sleep(600)
							time_count += 1
					continue
				else:
					time_count = 0
					likes_count[p['id']] = likes['summary']['total_count']
					while True:
						for like in likes['data']:
							if like['id'] not in who_likes_post:
								who_likes_post[like['id']] = []
							who_likes_post[like['id']].append(p['id'])  
						if 'paging' not in likes or 'next' not in likes['paging']:
							break
						likes = requests.get(likes['paging']['next']).json()
				
				comments = requests.get(api + p['id'] + '/comments?summary=true',params = para).json()
				if 'error' in comments:
					print 'comment error'
					comments_errors[p['id']] = comments['error']['message']
					if comments['error']['code'] == 17:
						if time_count < 3:
							time.sleep(600)
							time_count += 1
					continue
				else:
					time_count = 0
					comments_count[p['id']] = comments['summary']['total_count']
					while True:
						for comment in comments['data']:
							if comment['from']['id'] not in who_comment_post:
								who_comment_post[comment['from']['id']] = []
							who_comment_post[comment['from']['id']].append(p['id'])
							#print comment['from']['id'] + ' commented ' + p['id']
						if 'paging' not in comments or 'next' not in comments['paging']:
							break
						comments = requests.get(comments['paging']['next']).json()
						
			except ValueError as v:
				print 'returned value is not json'
				print api + p['id'] + '/likes?summary=true'
				continue
			except requests.exceptions.ConnectionError as e:
				print 'ConnectionFail'
				print api + p['id'] + '/likes?summary=true'
				continue
			if opts.test and count >= opts.test_size:
				break	
		if 'paging' not in r:
			break
		try:
			r = requests.get(r['paging']['next']).json()
		except ValueError as v:
			print 'returned value is not json'
			print r['paging']['next']
			continue
		except requests.exceptions.ConnectionError as e:
			print 'ConnectionFail'
			print r['paging']['next']
			continue
		print '%d posts scrapped' % count	
		if opts.test and count >= opts.test_size:
			break
	f.flush()
print 'compressing data'
shutil.make_archive('../../facebook/data', 'gztar', '../../facebook/data')
print 'compression completed'
#print 'deleting data directory'
#shutil.rmtree('data')
#print 'deletion completed'
for e in page_errors:
	print 'Error occurred while processing ' + e + ' page :' + page_errors[e]
for e in likes_errors:
	print 'Error occurred while obtaining likes on :' + e + ' post : ' + likes_errors[e] 
like_count_file = open(dest+'like_count','w')
like_file = open(dest+'who_likes_post','w')
comment_file = open(dest+'who_comments_post','w')
comment_count_file = open(dest+'comment_count','w')
share_file = open(dest+'share_count','w')
try:
	for share in share_count:
		share_file.write(share + ',' + str(share_count[share]) + '\n')
	for like in who_likes_post:
		like_file.write(like)
		for id in who_likes_post[like]:
			like_file.write(',' + id)
		like_file.write('\n')
	for comment in who_comment_post:
		comment_file.write(comment)
		for id in who_comment_post[comment]:
			comment_file.write(',' + id)
		comment_file.write('\n')
	for like in likes_count:	
		like_count_file.write(like + ',' + str(likes_count[like]) + '\n')
	for comment in comments_count:	
		comment_count_file.write(comment + ',' + str(comments_count[comment]) + '\n')
	for like in likes_errors:
		count = requests.get(api + likes_errors[like] + '/likes?summary=true',params = para).json()['summary']['total_count']
		like_count_file.write(like + ',' + str(count) + '\n')
except Exception as e:
	print "Error occurred while writing like file"