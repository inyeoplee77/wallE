# -*- coding: utf-8 -*-
import requests
import os
import locale
import time
import shutil

lines = open('../../data/facebook/tokens','r').read().split()
appID = lines[0]
#'931181156977094'
appSecret = lines[1]
#'9e7448f4765bb4455626f772da9a60e8'
token = lines[2]
#"EAANO54IVScYBADKZAODZAbPezJk1dZB54lnkvdLeQH1c0Mro72ZC714ZBYkSHW6OvDCUgcUGPRAhSTHpq1FI53lsZALnmvaQE0c3mxHYDK82J2Iyb27UgZBuntL7g2DpN8NhnijYQuKzCC4405hQzkDQumjHuOnsgP1tPB2dlm89gZDZD"


api = "https://graph.facebook.com/v2.5/"
para = {'access_token' : token}

f = open("../../data/facebook/bamboolist",'r')

pages = {}
for line in f:
	line = line.strip()
	line = line.split(',')
	pages[line[2]] = line[1]


likes_count = {}
comments_count = {}
who_likes_post = {}
who_comments_post = {}
share_count = {}
count = 0



for line in open("../../data/facebook/data/who_comments_post",'r'):
	line = line.strip()
	who_comments_post[line.split(',')[0]] = line.split(',')[1:]
for line in open("../../data/facebook/data/who_likes_post",'r'):
	line = line.strip()
	who_likes_post[line.split(',')[0]] = line.split(',')[1:]

for line in open("../../data/facebook/data/like_count",'r'):
	line = line.strip()
	likes_count[line.split(',')[0]] = int(line.split(',')[1])

for line in open("../../data/facebook/data/share_count",'r'):
	line = line.strip()
	share_count[line.split(',')[0]] = int(line.split(',')[1])

for line in open("../../data/facebook/data/comment_count",'r'):
	line = line.strip()
	comments_count[line.split(',')[0]] = int(line.split(',')[1])

				
def request(url):	
	r = requests.get(url,params=para).json()
	if 'error' in r:
		if r['error']['code'] == 17:
			while True:
				print 'wait for 600 seconds...'
				time.sleep(600)
				r = requests.get(url,params=para).json()
				if 'error' not in r:
					break
			return r
		else:
			return None
	else:
		return r				
		
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




if not os.path.exists(dest):
	os.makedirs(dest)
'''
else:
	y = raw_input('Would you like to clear data? (y/n)')
	if y =='y':
		shutil.rmtree(dest)
		os.makedirs(dest)
'''
for page in pages:
	debug = 'https://graph.facebook.com/debug_token?input_token=%s&access_token=%s'%(token, token)
	renew = 'https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=fb_exchange_token&fb_exchange_token=%s' % (appID, appSecret, token)
	dir = pages[page].split('/')[-1]
	dir = dest + dir
	count = 0
	if not os.path.exists(dir):
		os.makedirs(dir)
	r = request(api + page + "/posts")
	d = request(debug)
	if d['data']['expires_at'] < 3600:
		r = requests.get(renew)
		token = r.text.split(u'&')[0]			
		para = {'access_token' : token}
		
	while r is not None and 'previos' in r['paging']:
		r = request(r['paging']['previous'])	
	while True:
		try:
			if 'data' not in r:
				break
			for p in r['data']:
				if 'message' not in p:
					print 'message not in post'
					continue
				if not os.path.exists(dir+ '/' + p['id']):	
					f = open(dir+ '/' + p['id'],'w')
					f.write(p['message'].encode('utf8')) #save as byte form
				count += 1	
				share = request(api+p['id'] + '?fields=shares')
				if 'shares' in share:
					share_count[p['id']] = share['shares']['count']#int
				else:
					share_count[p['id']] = 0
				likes = request(api + p['id'] + '/likes?summary=true')
				likes_count[p['id']] = likes['summary']['total_count']
				while True:
					for like in likes['data']:
						if like['id'] not in who_likes_post:
							who_likes_post[like['id']] = []
						if p['id'] not in who_likes_post[like['id']]:
							who_likes_post[like['id']].append(p['id'])  
					if 'paging' not in likes or 'next' not in likes['paging']:
						break
					likes = request(likes['paging']['next'])
			
				comments = request(api + p['id'] + '/comments?summary=true')
				comments_count[p['id']] = comments['summary']['total_count']
				while True:
					for comment in comments['data']:
						if comment['from']['id'] not in who_comments_post:
							who_comments_post[comment['from']['id']] = []
						if p['id'] not in who_comments_post[comment['from']['id']]: 
							who_comments_post[comment['from']['id']].append(p['id'])
					if 'paging' not in comments or 'next' not in comments['paging']:
						break
					comments = request(comments['paging']['next'])
				f.close()
				if opts.test and count >= opts.test_size:
					break
		
		except:
			print 'some error occurred'
			continue
		print '%d posts scrapped' % count	
		if opts.test and count >= opts.test_size:
			break
		if 'paging' not in r or 'next' not in r['paging']:
			break	
		prev = r
		while True:
			try:
				r = request(prev['paging']['next'])
			except:
				print 'some error occurred'
				continue
			else:
				break
		
#print 'compressing data'
#shutil.make_archive(dest, 'gztar', dest)
#print 'compression completed'

like_count_file = open(dest+'like_count','w')
like_file = open(dest+'who_likes_post','w')
comment_file = open(dest+'who_comments_post','w')
comment_count_file = open(dest+'comment_count','w')
share_file = open(dest+'share_count','w')

for share in share_count:
	share_file.write(share + ',' + str(share_count[share]) + '\n')
for like in who_likes_post:
	like_file.write(like)
	for id in who_likes_post[like]:
		like_file.write(',' + id)
	like_file.write('\n')
for comment in who_comments_post:
	comment_file.write(comment)
	for id in who_comments_post[comment]:
		comment_file.write(',' + id)
	comment_file.write('\n')
for like in likes_count:	
	like_count_file.write(like + ',' + str(likes_count[like]) + '\n')
for comment in comments_count:	
	comment_count_file.write(comment + ',' + str(comments_count[comment]) + '\n')


f = open('../../data/facebook/tokens','w')
f.write(appID + ' ' + appSecret + ' ' token)
f.close()