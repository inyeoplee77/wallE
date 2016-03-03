# -*- coding: utf-8 -*-
import requests
appID = '719437504828313'
appSecret = 'dae1d765e81c02e566d6ccaa2b6af441'

token = "CAAKOUxjp05kBAM1Ay3YsOAzQIUZBmTw3JOk5U8CXzTy7h1ByIdmZBOoCZBz63YFbRPewFX3Ig4wyBCohQ3zB1TppS4duqNrgS0A2ZABgXZB6CmDDBpPpeIGJtnk3VkKFU40j3YK5N3dOct3Ji1SFCtUz6jOEfNcHu4eXko8CvjH6pxIKpp73Ufx9sfq86UZBdq6RqZCSYf6DwZDZD"

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


errors = {}

f = open("posts",'w')
for page in pages:
	r = requests.get(api + page + "/feed",params = para).json()
	posts[page] = []
	if 'error' in r or 'paging' not in r:
		print r.keys()
		print "Something went wrong"
		errors[page] = r
	#get all posts in the page and save in following format :  (post_id,content of post)\n(post_id,content)\n .... (just for the test)
	#
	#gonna change the format
	
	while 'previos' in r['paging']:
		r = requests.get(r['paging']['previous']).json()
	while 'next' in r['paging']:
		for p in r['data']:
			f.write( '(' + p['id'].encode('utf-8') + ',' + p['message'].encode('utf-8') +')' + '\n')
			#print requests.get(api + p['id'] + '/likes/' + page,params = para).json()
			#if requests.get(api + p['id'] + '/likes/' + page,params = para).json()['data']:
			#	print p['id'] + 'likes' + page
		r = requests.get(r['paging']['next']).json()
	
	#people who liked the post   {user_id}/likes/{post_id} check if key 'data' empty or not
	
	#count the number of likes for the post
	r = requests.get(api+page+'?fields=likes',params=para).json()['likes']
	print r
	#and whether he or she liked the page
	
	
	


