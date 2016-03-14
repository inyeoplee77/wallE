import os
import random
from shutil import copyfile
base = "facebook/"
train_target = "clustering/train/"
test_target = "clustering/test/"

shutil.rmtree('clustering/train')
shutil.rmtree('clustering/test')

os.mkdir(train_target)
os.mkdir(test_target)
for dir in os.listdir(base):
	if os.path.isdir(base + dir):
		files = random.sample(os.listdir(base + dir),2000)
		for f in files[:999]:
			copyfile(base + dir + "/" + f,train_target + f)
		for f in files[1000:]:
			copyfile(base + dir + "/" + f,test_target + f)				