import os
for file in os.listdir('result'):
	for line in open('result/' + file,'r'):
		print file
		id = '/'.join(line.strip().split('/')[1:])
		print open('../facebook/data/' + id).read()
		print '------------------------------------'
	print'===================================='