import os
import shutil
source = '../../data/result/raw_result/'
dest = '../../data/result/text_result'
if not os.path.exists(dest):
	os.mkdir(dest)
else:
	shutil.rmtree(dest)
	os.mkdir(dest)
for file in os.listdir(source):
	if os.path.exists(dest+'/'+file):
		shutil.rmtree(dest+'/'+file)
	os.mkdir(dest+'/'+file)
	print source + file
	for line in open(source + file,'r'):
		id = '/'.join(line.strip().split('/')[-2:])
		shutil.copyfile("../../data/facebook/data/" + id ,dest+'/'+file+ '/' + id.split('/')[-1])
	print 'done ' + file