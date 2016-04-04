import pickle
import operator
print 'load pickles'

'''
with open("../../data/HITS/auth.pickle", "rb") as input_file:
	auth = pickle.load(input_file)
with open("../../data/HITS/hub.pickle", "rb") as input_file:
	hub = pickle.load(input_file)
'''
univ_name = {
	'190747347803005':'CAU',
	'203051796562493':'HUFS',
	'580434565381308':'HYU',
	'1539168192989299':'KARTS',
	'497485933724583':'KNU',
	'206910909512230':'KOREA',
	'482012061908784':'KyungHee',
	'626784727386153':'SKKU',
	'560898400668463':'SNU',
	'413238928809895':'SoGang',
	'287555308059129':'UOS',
	'180446095498086':'Yonsei'
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
	f = open('../../data/HITS/result/'+univ_name[univ],'w')
	for r in result[univ]:
		f.write(str(r) + '\n')
	f.flush()
		