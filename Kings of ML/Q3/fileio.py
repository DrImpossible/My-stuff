from scipy import ndimage
import numpy as np
import skimage
from skimage.feature import (match_descriptors, corner_harris,corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
from skimage import img_as_uint
import h5py
from skimage.transform import resize
import cPickle as pickle

f = open('training_data.txt')
lines = f.read().split('\n')[1:-1]

train_labels=[]
train_imdb=[]
train_desc=[]
cnt = 0

for line in lines:
	line = line.split(':')
	print line
#	cnt+=1
#	if cnt>20:
#		break
	train_labels.append(line[1])
	im =  img_as_uint(rgb2gray(ndimage.imread(line[2])))
	im = resize(im, (512, 512))
	train_imdb.append(im)

#train_imdb = np.asarray(train_imdb)
#train_labels = np.asarray(train_labels)

f = open('testing_data.txt')
lines = f.read().split('\n')[1:-1]

test_labels=[]
test_imdb=[]
test_desc=[]

for line in lines:
	line = line.split(':')
	print line
#	cnt+=1
#	if cnt>20:
#		break
	test_labels.append(line[1])
	im =  img_as_uint(rgb2gray(ndimage.imread(line[2])))
	im = resize(im, (512, 512))
	test_imdb.append(im)

#test_imdb = np.asarray(test_imdb)

descriptor_extractor = ORB(n_keypoints=20)

print('Starting...')
for i in xrange(len(train_labels)):
	print(i)
	descriptor_extractor.detect_and_extract(train_imdb[i])
	keypoints = descriptor_extractor.keypoints
	train_desc.append(descriptor_extractor.descriptors)

for i in xrange(len(test_imdb)):
	print(i)
	descriptor_extractor.detect_and_extract(test_imdb[i])
	keypoints = descriptor_extractor.keypoints
	test_desc.append(descriptor_extractor.descriptors)
#
#matches12 = match_descriptors(train_desc[0], train_desc[1], cross_check=True)
#print(len(matches12))
#print(matches12.shape)
output = open('train_data_3.pkl', 'wb')
pickle.dump(train_desc, output)
output.close()

output = open('train_labels.pkl', 'wb')
pickle.dump(train_labels, output)
output.close()

output = open('test_data_3.pkl', 'wb')
pickle.dump(test_desc, output)
output.close()