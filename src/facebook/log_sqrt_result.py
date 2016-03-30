import os
import math
from operator import mul
import operator
def sig(x):
	return (1/ (1+math.exp(-x)))# * 200000 - 100000 # 0~100000. Failed
def absf(x):
	return (x / (1+abs(x))) * 100 #0~100

share_file = open('../../data/facebook/shares_sorted','r')
comment_file = open('../../data/facebook/comment_count_sorted','r')
like_file = open('../../data/facebook/like_count_sorted','r')

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
sqrt_result = open('../../data/facebook/sqrt_result','w')
log_result = open('../../data/facebook/log_result','w')

for t in sqrt_sorted:
	#t[0] == id
	#t[1] == score
	sqrt_result.write(t[0] + ',' + str(t[1]) + '\n')
for t in log_sorted:
	log_result.write(t[0] + ',' + str(t[1]) + '\n')




