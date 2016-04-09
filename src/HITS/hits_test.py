import pickle
import operator
import shutil
import os
print 'load pickles'

'''
with open("../../data/HITS/auth.pickle", "rb") as input_file:
	auth = pickle.load(input_file)
with open("../../data/HITS/hub.pickle", "rb") as input_file:
	hub = pickle.load(input_file)
'''
univ_name = {
	'190747347803005':'caubamboo',
	'203051796562493':'hufsbamboo',
	'580434565381308':'hyubamboo',
	'1539168192989299':'kartsbamboo',
	'497485933724583':'KNUbamboo',
	'206910909512230':'koreabamboo',
	'482012061908784':'kyungheebamboo',
	'626784727386153':'SKKUBamboo',
	'560898400668463':'SNUBamboo',
	'413238928809895':'sogangbamboo',
	'287555308059129':'uosbamboo',
	'180446095498086':'yonseibamboo'
}



with open("../../data/HITS/auth_score.pickle", "rb") as input_file:
	auth_score = pickle.load(input_file)
with open("../../data/HITS/hub_score.pickle", "rb") as input_file:
	hub_score = pickle.load(input_file)
print 'load complete'
print 'sorting authorities'

auth_sorted = sorted(auth_score.items(),key =operator.itemgetter(1),reverse = True)

print 'sorting complete'


univs = {}
result = {}
for a in auth_sorted:
	univ = a[0].split('_')[0]
	if univ not in univs:
		result[univ] = []
		univs[univ] = 40
	if univs[univ] != 0:
		result[univ].append(a[0])
		univs[univ] -= 1
for univ in result:
	if not os.path.exists('../../data/HITS/result/'+univ_name[univ]): 
		os.mkdir('../../data/HITS/result/'+univ_name[univ])
	for r in result[univ]:
		shutil.copyfile('../../data/facebook/data/'+ univ_name[univ] + '/' + r,'../../data/HITS/result/' + univ_name[univ] + '/' + r)
		