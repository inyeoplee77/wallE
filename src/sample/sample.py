import os
import random
import shutil
import tarfile
from optparse import OptionParser

op = OptionParser('sample.py [options]\nno option, copy samples of data from cooked data')
op.add_option("--raw",help="copy samples of data from raw data",dest="raw",action='store_true',default=False)
op.add_option("--n-samples",type=int,default=1000,dest="size",help="size of sample. default = 1000")
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
	op.error("this script takes no arguments.")
	sys.exit(1)

if opts.raw:
    base = "../../data/facebook/data/"
    print 'raw data'
else:
    base = "../../data/nlp/data/"
    print 'cooked data'
sample_size = opts.size



train_target = "../../data/training/train/"
test_target = "../../data/training/test/"


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
