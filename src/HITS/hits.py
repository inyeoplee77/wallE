import math
import pickle
import os
def hits(hub,auth,hub_score,auth_score,steps):
	
	for i in range(steps):
		error = diff   
		norm = 0
		for a in auth:
			v = auth_score[a]
			auth_score[a] = 0
			for h in auth[a]:
				auth_score[a] += hub_score[h]
			diff += abs(v - auth_score[a])
			norm += auth_score[a] ** 2
		norm = math.sqrt(norm)
		for a in auth:
			auth_score[a] = auth_score[a] / norm
			
		norm = 0
		for h in hub:
			v = hub_score[h]
			hub_score[h] = 0
			for a in hub[h]:
				hub_score[h] += auth_score[a]
			diff += abs(v - hub_score[h])
			norm += hub_score[h] ** 2
		norm = math.sqrt(norm)
		for h in hub:
			hub_score[h] = hub_score[h] / norm
		print 'iteration ' + str(i) + ' done'
		print 'error: %d' % abs(diff - error)
		if abs(diff-error) < 0.1:
			break
	return hub,auth,hub_score,auth_score



def initialize(auth,hub):
	if os.path.exists('auth.pickle') and os.path.exists('hub.pickle'):
		with open(r"auth.pickle", "rb") as input_file:
			auth = pickle.load(input_file)
		with open(r"hub.pickle", "rb") as input_file:
			hub = pickle.load(input_file)
	else:	
		for line in open('../../data/facebook/data/who_likes_post','r'):
			line = line.strip()
			hub[line.split(',')[0]] = line.split(',')[1:]
			for i in line.split(',')[1:]:
				if i not in auth:
					auth[i] = []
				auth[i].append(line.split(',')[0])

		for line in open('../../data/facebook/data/who_comments_post','r'):
			line = line.strip()
			if line.split(',')[0] not in hub:
				hub[line.split(',')[0]] = line.split(',')[1:]
			else:
				hub[line.split(',')[0]].extend(line.split(',')[1:])
			
			for i in line.split(',')[1:]:
				if i not in auth:
					auth[i] = []
				auth[i].append(line.split(',')[0])
	return auth,hub
auth = {}
hub = {}
auth,hub = initialize(auth,hub)		
auth_score = dict.fromkeys(auth,1)
hub_score = dict.fromkeys(hub,1)

print 'load complete'
print 'initiate hits algorithm' 
	
hub,auth,hub_score,auth_score = hits(hub,auth,hub_score,auth_score,10)
		
print 'hits algorithm done'

print 'pickle objects'
with open('hub.pickle', 'wb') as h:
	pickle.dump(hub, h)
with open('auth.pickle', 'wb') as h:
	pickle.dump(auth, h)
with open('hub_score.pickle', 'wb') as h:
	pickle.dump(hub_score, h)
with open('auth_score.pickle', 'wb') as h:
	pickle.dump(auth_score, h)
print 'pickling done'
