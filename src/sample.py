import os
import random
import shutil
import tarfile
base = "data/"
train_target = "clustering/train/"
test_target = "clustering/test/"
sample_size = 1000

if os.path.exists(train_target):
	shutil.rmtree(train_target)
if os.path.exists(test_target):
	shutil.rmtree(test_target)
os.mkdir(train_target)
os.mkdir(test_target)

if not os.path.exists(base):
	tarfile.open(base[:-1] + '.tar.gz','r').extractall(base)
	 
for dir in os.listdir(base):	
	if os.path.isdir(base + dir):
		print "copying samples of " + dir + " data..." 
		files = random.sample(os.listdir(base + dir),sample_size * 2)
		if not os.path.exists(train_target + dir):
			os.mkdir(train_target + dir)
			os.mkdir(test_target + dir)
		for f in files[:sample_size]:
			shutil.copyfile(base + dir + "/" + f,train_target + dir + '/' + f)
		for f in files[sample_size:]:
			shutil.copyfile(base + dir + "/" + f,test_target +  dir + '/'+ f)
print "copy complete"
