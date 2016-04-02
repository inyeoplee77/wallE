import pickle
import operator
print 'load pickles'

'''
with open(r"auth.pickle", "rb") as input_file:
	auth = pickle.load(input_file)
with open(r"hub.pickle", "rb") as input_file:
	hub = pickle.load(input_file)
'''
with open(r"auth_score.pickle", "rb") as input_file:
	auth_score = pickle.load(input_file)
with open(r"hub_score.pickle", "rb") as input_file:
	hub_score = pickle.load(input_file)
print 'load complete'
print 'sorting authorities'
auth_sorted = sorted(auth_score.items(),key =operator.itemgetter(1),reverse = True)
print 'sorting complete'
for a in auth_sorted[:1000]:
	print a[0],a[1]