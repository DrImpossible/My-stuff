import h5py
import numpy as np

f=open('training_set_shuffled.csv')
lines=f.read().split('\n')[:-1]

labels = []
master_dic = []
master_cnt = []
values = []
no_values = []
sumval = []

for i in xrange(61):
    values.append([])
    sumval.append(0.0)
    master_cnt.append(0)
    master_dic.append({})
#print len(values)

for i in xrange(len(lines)):
    lines[i]=lines[i].split(',')
    labels.append(lines[i][-1])
    lines[i]=lines[i][:-1]
    for j in xrange(len(lines[i])):
        values[j].append(lines[i][j])

for i in xrange(len(lines[0])):
    no_values.append(len(set(values[i])))

for j in xrange(len(lines[0])):
    for i in xrange(len(lines)):
        if no_values[j]<10000:            
            if lines[i][j] not in master_dic[j]:
                master_dic[j][lines[i][j]]=master_cnt[j]
                master_cnt[j]+=1

            lines[i][j]=master_dic[j][lines[i][j]]

for i in xrange(len(lines[0])):
    count=0.0
    flag=0
    for j in xrange(len(lines)):
        sumval[i]=sumval[i]+float(lines[j][i])
        count+=1
        #print i

    sumval[i]/=count

    for j in xrange(len(lines)):
        lines[j][i]=float(lines[j][i])-sumval[i]

lines=np.array(lines)
labels=np.array(labels)

h5f = h5py.File('train_data.h5', 'w')
h5f.create_dataset('dataset', data=lines)
h5f.close()

h5f = h5py.File('train_labels.h5', 'w')
h5f.create_dataset('dataset', data=labels)
h5f.close()

f=open('testing_set.csv')
lines=f.read().split('\n')[:-1]

values = []

for i in xrange(61):
    values.append([])
#print len(values)

for i in xrange(len(lines)):
    lines[i]=lines[i].split(',')
    for j in xrange(len(lines[i])):
        values[j].append(lines[i][j])
recall_idx = []
for j in xrange(len(lines[0])):
    for i in xrange(len(lines)):
        if no_values[j]<10000:            
            if lines[i][j] not in master_dic[j]:
                recall_idx.append(i)
                master_dic[j][lines[i][j]]=master_cnt[j]
                master_cnt[j]+=1

            lines[i][j]=master_dic[j][lines[i][j]]

for i in xrange(len(lines[0])):
    for j in xrange(len(lines)):
        lines[j][i]=float(lines[j][i])-sumval[i]

lines=np.array(lines)
print(set(recall_idx))

h5f = h5py.File('test_data.h5', 'w')
h5f.create_dataset('dataset', data=lines)
h5f.close()