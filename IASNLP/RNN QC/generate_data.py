import gzip
import cPickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
f = gzip.open('qclirothdataset.pkl.gz', 'rb')
train_set,valid_set, test_set = cPickle.load(f)
enc = OneHotEncoder(dtype=np.int16,sparse=False)
enc.fit([[1],[0],[2],[3],[4],[0],[1],[4],[3],[5],[5],[4],[3]])
m3=[]
for val in test_set[1]:
    #print enc.transform([val])
    m3.append(enc.transform([[val]])[0])
    
m1=[]
for val in train_set[1]:
    m1.append(enc.transform([[val]])[0])
    
train_set = train_set[0], m1
test_set = test_set[0], m3

dataset = [train_set,[], test_set]

f = gzip.open('encodeddataset.pkl.gz','wb')
cPickle.dump(dataset, f, protocol=2)
f.close()

