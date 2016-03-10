# -*- coding: utf-8 -*-
import requests
import os
import re
import locale
appID = '719437504828313'
appSecret = 'dae1d765e81c02e566d6ccaa2b6af441'

token = "CAAKOUxjp05kBAGv2nl1XKZBWBp7bfyStp2FhRTzJTV3xJZBObadaYBSDyEEGDTezs81XofaYEbPtMdcBTwYHZCi99wHjuX6VWCNJesM6jEtF6UxhtqvHIidpGBm6u4pXnDuNFwpLjLl9HEqjJwIUI0ZBN4iJx57Tzu3qdoGZCuZB6LwdAf3816"

#token = "CAAKOUxjp05kBAMd0ihtkaLKrkjZAAZBkwUcSl1VOjdHypVyqgH4lIuaXjWfMdXNDgD4oEGA8FMMj8m2WjX9S9YmPOrbo67jypUki3eKtWln5wwGVMjvsb7mMLzAq8ZCTPYm7vkKm68uYJ9asTAb2JC77ntMnV8CATnGLAYLkZAjZA3nTzvOdfG4dOYMEf9LBs5C9uGYTNjwZDZD"

api = "https://graph.facebook.com/v2.5/"
para = {'access_token' : token}

f = open("bamboolist",'r')

pages = {}
for line in f:
	line = line.strip()
	line = line.split(',')
	pages[line[2]] = line[1]
posts = {}
page_errors = {}
likes_errors = []
likes = {}
count = 0

#locale.setlocale(locale.LC_ALL,'')
#[^ ㄱ-ㅎ|ㅏ-ㅣㅣ가-힣]+
nonkorean = re.compile('[^ 가-힣]+')
hashtag = re.compile('#[가-힣\w0-9\S]+')
<<<<<<< HEAD
nomean = re.compile('[ㄱ-ㅎ]')
print pages
=======
nomean = re.compile('[ㄱ-ㅎ]+')
print nomean.sub('','뭐야 이거ㅋㅋㅋㅋ')
>>>>>>> b639149ddcde32615ff1234ee58681cf9e50d6ca
for page in pages:
	dir = pages[page].split('/')[-1]
	print dir
	count = 0
	if not os.path.exists(dir):
		os.makedirs(dir)
	r = requests.get(api + page + "/posts",params = para).json()
	if 'error' in r:
		page_errors[page] = r['error']['message']
		continue
	while 'previos' in r['paging']:
		r = requests.get(r['paging']['previous']).json()
	while 'paging' not in r.keys() or 'next' in r['paging']:
		for p in r['data']:
			f = open(dir+ '/' + p['id'],'w')
			if 'message' not in p:
				continue
			message = nomean.sub('',p['message']).encode('utf8').strip()
			message = ' '.join(nonkorean.sub('',hashtag.sub('',message)).split())
			f.write(message.strip())
			count += 1
			like = requests.get(api + p['id'] + '/likes?summary=true',params = para).json()
			if 'error' in like:
				likes_errors.append(p['id']) 
				continue
			else:
				likes[p['id']] = like['summary']['total_count']
		if 'paging' not in r.keys():
			break
		r = requests.get(r['paging']['next']).json()
		print '%d posts scrapped' % count
			
for e in page_errors:
	print 'Error occurred while processing ' + e + 'page :' + page_errors[e]
for e in likes_errors:
	print 'Error occurred while obtaining likes on post' + e
f = open('likes','w')
for like in likes:
	f.write(like+' ' + likes[like] + '\n')
	


