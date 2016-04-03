import os
import math
from operator import mul
import operator
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def sig(x):
	return (1/ (1+math.exp(-x)))# * 200000 - 100000 # 0~100000. Failed
def absf(x):
	return (x / (1+abs(x))) * 100 #0~100
def draw_distribution(data):
	fit = stats.norm.pdf(data, np.mean(data), np.std(data))
	plt.plot(data,fit,'-o')
	plt.hist(data,normed=True)
	plt.show()



share_file = open('../../data/facebook/data/share_count','r')
comment_file = open('../../data/facebook/data/comment_count','r')
like_file = open('../../data/facebook/data/like_count','r')

result_dict = {}
for line in share_file:
	line = line.strip()
	line = line.split(',')
	result_dict[line[0]] = [int(line[1])+1]
for line in comment_file:
	line = line.strip()
	line = line.split(',')
	result_dict[line[0]].append(int(line[1])+1)
for line in like_file:
	line = line.strip()
	line = line.split(',')
	result_dict[line[0]].append(int(line[1]))

		
korea = '206910909512230'


#likes_korea = {}

for univ in univs:
	likes = map(lambda x : x[1],filter(lambda x : x[0].split('_')[0] == univ,map(lambda x : (x,result_dict[x][2]),result_dict)))
	likes.sort(reverse = True)
		
#print likes_korea
#likes = map(lambda x : likes_korea[x][0],likes_korea)
#likes = filter(lambda x : x.split('_')[0] == korea,likes)#likes[x] > 1000 and x.split('_')[0] == korea)
#comments = filter(lambda x : x > 47,map(lambda x : result_dict[x][1],result_dict))
#shares = filter(lambda x : x > 90,map(lambda x : result_dict[x][0],result_dict))


#comments.sort()
#shares.sort()


#print np.mean(comments)
#print np.mean(shares)

print len(likes)
draw_distribution(likes) 



'''	
#{"id" : [1,2,3]}
sqrt_score = {}
log_score = {}
for i in result_dict:
	sqrt_score[i] = math.sqrt(reduce(mul,result_dict[i],1))

for i in result_dict:
	s = [math.log(x+1) for x in result_dict[i]]
	log_score[i] = reduce(mul, s, 1) #math.log(reduce(mul,result_dict[i],1))



sqrt_sorted = sorted(sqrt_score.items(),key = operator.itemgetter(1),reverse = True)
log_sorted = sorted(log_score.items(),key = operator.itemgetter(1),reverse = True)
sqrt_result = open('sqrt_result','w')
log_result = open('log_result','w')

for t in sqrt_sorted:
	#t[0] == id
	#t[1] == score
	sqrt_result.write(t[0] + ',' + str(t[1]) + '\n')
for t in log_sorted:
	log_result.write(t[0] + ',' + str(t[1]) + '\n')
'''