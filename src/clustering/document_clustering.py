# -*- coding: utf-8 -*-
'''
=======================================
Clustering text documents using k-means
=======================================

This is an example showing how the scikit-learn can be used to cluster
documents by topics using a bag-of-words approach. This example uses
a scipy.sparse matrix to store the features instead of standard numpy arrays.

Two feature extraction methods can be used in this example:

  - TfidfVectorizer uses a in-memory vocabulary (a python dict) to map the most
	frequent words to features indices and hence compute a word occurrence
	frequency (sparse) matrix. The word frequencies are then reweighted using
	the Inverse Document Frequency (IDF) vector collected feature-wise over
	the corpus.

  - HashingVectorizer hashes word occurrences to a fixed dimensional space,
	possibly with collisions. The word count vectors are then normalized to
	each have l2-norm equal to one (projected to the euclidean unit-ball) which
	seems to be important for k-means to work in high dimensional space.

	HashingVectorizer does not provide IDF weighting as this is a stateless
	model (the fit method does nothing). When IDF weighting is needed it can
	be added by pipelining its output to a TfidfTransformer instance.

Two algorithms are demoed: ordinary k-means and its more scalable cousin
minibatch k-means.

Additionally, latent sematic analysis can also be used to reduce dimensionality
and discover latent patterns in the data. 

It can be noted that k-means (and minibatch k-means) are very sensitive to
feature scaling and that in this case the IDF weighting helps improve the
quality of the clustering by quite a lot as measured against the "ground truth"
provided by the class label assignments of the 20 newsgroups dataset.

This improvement is not visible in the Silhouette Coefficient which is small
for both as this measure seem to suffer from the phenomenon called
"Concentration of Measure" or "Curse of Dimensionality" for high dimensional
datasets such as text data. Other measures such as V-measure and Adjusted Rand
Index are information theoretic based evaluation scores: as they are only based
on cluster assignments rather than distances, hence not affected by the curse
of dimensionality.

Note: as k-means is optimizing a non-convex objective function, it will likely
end up in a local optimum. Several runs with independent random init might be
necessary to get a good convergence.
'''

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause

from __future__ import print_function

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import NMF, LatentDirichletAllocation
import logging
from optparse import OptionParser
import sys
import os
import shutil
from time import time
from scipy.sparse import csr_matrix
import numpy as np


# Display progress logs on stdout
#logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--lsa",
			  dest="n_components", type="int",
			  help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
			  action="store_false", dest="minibatch", default=True,
			  help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
			  action="store_false", dest="use_idf", default=True,
			  help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
			  action="store_true", default=False,
			  help="Use a hashing feature vectorizer")
'''
op.add_option("--n-features", type=int, default=10000,
			  help="Maximum number of features (dimensions)"
				   " to extract from text.")
'''
op.add_option("--verbose",
			  action="store_true", dest="verbose", default=False,
			  help="Print progress reports inside k-means algorithm.")

#print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
	op.error("this script takes no arguments.")
	sys.exit(1)

#raw_input()
###############################################################################
# Load some categories from the training set
'''
categories = [
	'alt.atheism',
	'talk.religion.misc',
	'comp.graphics',
	'sci.space',
]
'''


#stop_words = [u'외대',u'한양대',u'고대', u'연대',u'중앙대',u'경북대',u'경희대',u'서울대',u'설대',u'성대',u'성균관대',u'서강대',u'서울시립대',u'댓글',u'시립대',u'서울시립대',u'오전',u'오후',u'외침',u'제보',u'숲',u'대숲',u'대나무숲',u'연대숲',u'서강대숲',u'이야기']
# Uncomment the following to do the analysis on all the categories
categories = None

#dataset = fetch_20newsgroups(subset='train', categories=categories,
#                            shuffle=True, random_state=42)

################
#original = load_files('../facebook/data')
cache = dict(train=load_files('../../data/training/train',encoding = 'utf8'),test=load_files('../../data/training/test/',encoding='utf8'))
data_lst = list()
target = list()
filenames = list()
for subset in ('train', 'test'):
	data = cache[subset]
	data_lst.extend(data.data)
	target.extend(data.target)
	filenames.extend(data.filenames)
data.data = data_lst
data.target = np.array(target)
data.filenames = np.array(filenames)
dataset = data
################
print("%d documents" % len(dataset.data))
print("%d categories" % len(dataset.target))
print()
#labels = dataset.target
true_k = 2
print 
#true_k = np.unique(labels).shape[0]

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()
if opts.use_hashing:
	if opts.use_idf:
		# Perform an IDF normalization on the output of HashingVectorizer
		hasher = HashingVectorizer(n_features=opts.n_features,
									non_negative=True,
								   norm=None, binary=False)
		vectorizer = make_pipeline(hasher, TfidfTransformer())
	else:
		vectorizer = HashingVectorizer(n_features=opts.n_features,
									   non_negative=False, norm='l2',
									   binary=False)
else:
	vectorizer = TfidfVectorizer(max_df=0.1, #max_features=opts.n_features,
								 min_df=1,
								 use_idf=opts.use_idf,encoding='utf8')
X = vectorizer.fit_transform(dataset.data)

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()
print(X.shape)
if opts.n_components:
	print("Performing dimensionality reduction using LSA")
	t0 = time()
	# Vectorizer results are normalized, which makes KMeans behave as
	# spherical k-means for better results. Since LSA/SVD results are
	# not normalized, we have to redo the normalization.
	svd = TruncatedSVD(opts.n_components)
	normalizer = Normalizer(copy=False)
	lsa = make_pipeline(svd, normalizer)

	X = lsa.fit_transform(X)

	print("done in %fs" % (time() - t0))

	explained_variance = svd.explained_variance_ratio_.sum()
	print("Explained variance of the SVD step: {}%".format(
		int(explained_variance * 100)))

	print()


###############################################################################
# Do the actual clustering

#if opts.minibatch:
#	km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,init_size=1000, batch_size=1000, verbose=opts.verbose)

#else:
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=10,verbose=opts.verbose)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(X)
print("done in %0.3fs" % (time() - t0))
print()
'''
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
print("Adjusted Rand-Index: %.3f"
	  % metrics.adjusted_rand_score(labels, km.labels_))
print("Silhouette Coefficient: %0.3f"
	  % metrics.silhouette_score(X, km.labels_, sample_size=60))
'''
print()

if not opts.use_hashing:
	print("Top terms per cluster:")

	if opts.n_components:
		original_space_centroids = svd.inverse_transform(km.cluster_centers_)
		order_centroids = original_space_centroids.argsort()[:, ::-1]
	else:
		order_centroids = km.cluster_centers_.argsort()[:, ::-1]

	terms = vectorizer.get_feature_names()
	for i in range(true_k):
		print("Cluster %d:" % i, end='')
		for ind in order_centroids[i, :10]:
			print(' %s' % terms[ind], end='\n')
		print()





#LDA
n_samples = X.shape[0]
n_features = X.shape[1]
n_topics = 10
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
	for topic_idx, topic in enumerate(model.components_):
		print("Topic #%d:" % topic_idx)
		print(" ".join([feature_names[i]
						for i in topic.argsort()[:-n_top_words - 1:-1]]))
	print()


print("Loading dataset...")
t0 = time()

data_samples = dataset.data
tfidf_vectorizer = vectorizer
print("done in %0.3fs." % (time() - t0))
'''
# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
#tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,decode_error = 'ignore')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
'''
# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
#tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features)
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,binary = True)
#tf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features)
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
'''
# Fit the NMF model
print("Fitting the NMF model with tf-idf features,"
	  "n_samples=%d and n_features=%d..."
	  % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)
'''
print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
	  % (n_samples, n_features))

lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=10,learning_method='batch')
t0 = time()
result = lda.fit_transform(tf)
print("done in %0.3fs." % (time() - t0))


print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)



#number of clusters
clusters = 2


km = KMeans(n_clusters=clusters, init='k-means++', max_iter=100, n_init=10,verbose=opts.verbose)

result = csr_matrix(result)
km.fit(result)

dest = '../../data/result/raw_result'
if not os.path.exists(dest):
	os.mkdir(dest)
else:
	shutil.rmtree(dest)
	os.mkdir(dest)
#order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(clusters):
	print("Cluster %d:" % i, end='')
	d = km.transform(result)[:, i]
	ind = np.argsort(d)[::-1][:10]
	f = open(dest +'/cluster' + str(i),'w')	
	for index in ind:
		print(' %s' % index, end='\n')
		f.write(dataset.filenames[index] + '\n')