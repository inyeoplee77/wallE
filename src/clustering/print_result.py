import os
import shutil
if not os.path.exists('text_result'):
	os.mkdir('text_result')
else:
	shutil.rmtree('text_result')
	os.mkdir('text_result')
for file in os.listdir('result'):
	if os.path.exists('text_result/'+file+'_text'):
		shutil.rmtree('text_result/'+file+'_text')
	os.mkdir('text_result/'+file+'_text')
	for line in open('result/' + file,'r'):
		id = '/'.join(line.strip().split('/')[1:])
		shutil.copyfile("../facebook/data/" + id ,'text_result/'+file+'_text/' + id.split('/')[-1])
	print 'done ' + file