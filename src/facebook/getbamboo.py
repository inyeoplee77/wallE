# -*- coding: utf-8 -*-
import requests
import os
import re
import locale
import time
import shutil
appID = '719437504828313'
appSecret = 'dae1d765e81c02e566d6ccaa2b6af441'

token = "CAAKOUxjp05kBAGv2nl1XKZBWBp7bfyStp2FhRTzJTV3xJZBObadaYBSDyEEGDTezs81XofaYEbPtMdcBTwYHZCi99wHjuX6VWCNJesM6jEtF6UxhtqvHIidpGBm6u4pXnDuNFwpLjLl9HEqjJwIUI0ZBN4iJx57Tzu3qdoGZCuZB6LwdAf3816"

#token = "CAAKOUxjp05kBAMd0ihtkaLKrkjZAAZBkwUcSl1VOjdHypVyqgH4lIuaXjWfMdXNDgD4oEGA8FMMj8m2WjX9S9YmPOrbo67jypUki3eKtWln5wwGVMjvsb7mMLzAq8ZCTPYm7vkKm68uYJ9asTAb2JC77ntMnV8CATnGLAYLkZAjZA3nTzvOdfG4dOYMEf9LBs5C9uGYTNjwZDZD"

api = "https://graph.facebook.com/v2.5/"
para = {'access_token' : token}

f = open("bamboolist_test",'r')

pages = {}
for line in f:
	line = line.strip()
	line = line.split(',')
	pages[line[2]] = line[1]
posts = {}
page_errors = {}
likes_errors = {}
likes = {}
count = 0

#locale.setlocale(locale.LC_ALL,'')
#[^ ㄱ-ㅎ|ㅏ-ㅣㅣ가-힣]+
nonkorean = re.compile(u'[^ 가-힣]+',re.UNICODE)
hashtag = re.compile(u'#[가-힣\w0-9\S]+',re.UNICODE)
nomean = re.compile(u'[ㄱ-ㅎ]|[가-힣\S]*대숲|[가-힣\S]*대나무숲|[0-9\S]*번째|[가-힣\S]*학교',re.UNICODE)
#print pages
time_count = 0
if not os.path.exists('data'):
	os.makedirs('data')
for page in pages:
	dir = pages[page].split('/')[-1]
	dir = 'data/' + dir
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
				continue
			message = nomean.sub(u' ',p['message'].strip())
			message = u' '.join([voc for voc in nonkorean.sub(u'',hashtag.sub('',message)).split() if len(voc) < 10])
			f.write(message.encode('utf8')) #save as byte form
			
			#message = nomean.sub('',p['message']).encode('utf8').strip()
			#message = ' '.join(nonkorean.sub('',hashtag.sub('',message)).split())
			#f.write(message.strip().encode('utf8'))
			count += 1
			try:
				like = requests.get(api + p['id'] + '/likes?summary=true',params = para).json()
				if 'error' in like:
					likes_errors[p['id']] = like['error']['message']
					if like['error']['code'] == 17:
						if time_count < 3:
							time.sleep(600)
							time_count += 1
					continue
				else:
					time_count = 0
					likes[p['id']] = like['summary']['total_count']
			except ValueError as v:
				print 'returned value is not json'
				print api + p['id'] + '/likes?summary=true'
				continue
			except requests.exceptions.ConnectionError as e:
				print 'ConnectionFail'
				print api + p['id'] + '/likes?summary=true'
				continue
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
		#if count >= 100:
		#	break
	f.flush()

print 'compressing data'
shutil.make_archive('data', 'gztar', 'data')
print 'compression completed'		
#print 'deleting data directory'
#shutil.rmtree('data')
#print 'deletion completed'
for e in page_errors:
	print 'Error occurred while processing ' + e + ' page :' + page_errors[e]
for e in likes_errors:
	print 'Error occurred while obtaining likes on :' + e + ' post : ' + likes_errors[e] 
like_file = open('likes','w')
try:
	for like in likes:	
		like_file.write(like + ' ' + str(likes[like]) + '\n')
	for like in likes_errors:
		count = requests.get(api + likes_errors[like] + '/likes?summary=true',params = para).json()['summary']['total_count']
		like_file.write(like + ' ' + str(count) + '\n')
except Exception as e:
	print "Error occurred while writing like file"


