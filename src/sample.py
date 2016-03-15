import os
import random
import shutil
base = "facebook/"
train_target = "clustering/train/"
test_target = "clustering/test/"
if os.path.exists(train_target):
	shutil.rmtree(train_target)
if os.path.exists(test_target):
	shutil.rmtree(test_target)
os.mkdir(train_target)
os.mkdir(test_target)
for dir in os.listdir(base):	
	if os.path.isdir(base + dir):
		print "copying samples of " + dir + " data..." 
		files = random.sample(os.listdir(base + dir),2000)
		for f in files[:1000]:
			shutil.copyfile(base + dir + "/" + f,train_target + f)
		for f in files[1000:]:
			shutil.copyfile(base + dir + "/" + f,test_target + f)
print "copy complete"