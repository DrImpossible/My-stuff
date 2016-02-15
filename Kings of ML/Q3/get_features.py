from skimage.feature import match_descriptors
import cPickle as pickle

#img1 = img_as_uint(rgb2gray(ndimage.imread('./data/1.jpg')))
#img2 = img_as_uint(rgb2gray(ndimage.imread('./data/2.jpg')))
#
#descriptor_extractor = ORB(n_keypoints=1000)
#descriptor_extractor.detect_and_extract(img1)
#keypoints1 = descriptor_extractor.keypoints
#descriptors1 = descriptor_extractor.descriptors
#
#descriptor_extractor.detect_and_extract(img2)
#keypoints2 = descriptor_extractor.keypoints
#descriptors2 = descriptor_extractor.descriptors
#
#matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

inp = open('./data/train_data_2.pkl', 'rb')
train_descs=pickle.load(inp)
inp.close()

inp = open('./data/test_data_2.pkl', 'rb')
test_descs=pickle.load(inp)
inp.close()

inp = open('./data/train_labels.pkl', 'rb')
train_labels=pickle.load(inp)
inp.close()

f=open('testSubmission.csv')
lines=f.read().split('\n')

print('IDVal,Type,File_Name')
	
idx=0
cnt=0
label=[]
desc_test=[]
for test_desc in test_descs:
	cnt+=1
	label=[]
	for i in xrange(len(train_descs)):
		matches = match_descriptors(test_desc, train_descs[i], cross_check=True)
		num_matches = matches.shape[0]
		avg_match = sum(matches[:,1])/float(num_matches)
		label.append([num_matches*avg_match,i])

	label = train_labels[(sorted(label, key=lambda x: x[0])[0])[1]]
	line = lines[cnt].split(',')
	print(line[0]+','+str(label)+','+line[2])