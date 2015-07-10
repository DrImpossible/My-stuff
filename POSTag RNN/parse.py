#def fuckyou():
if 1==1:
    fp=open('hindi_trainingdata.txt')
    hindidata=[]
    labels=[]

    for i in fp:
        i=i.strip('\n').split(' ')
        for j in i:
            if j!='':
                ans=j.split('_')
                hindidata.append(ans[0])
                labels.append(ans[1])
                
    hindidict={}
    labelsdict={}
    cnt=0
    for i in hindidata:
        if i not in hindidict:
            hindidict[i]=cnt
            cnt+=1
        
    cnt=0
    for i in labels:
        if i not in labelsdict:
            labelsdict[i]=cnt
            cnt+=1
       
    print len(hindidata)
    print len(labels)
    
    for i in xrange(len(hindidata)):
        hindidata[i]=hindidict[hindidata[i]]
        
    for i in xrange(len(labels)):
        labels[i]=labelsdict[labels[i]]
           
    #print hindidata[0:10]
    #print labels[0:10]
    
    testdata = hindidata[2000:3000]
    validdata = hindidata[3001:3300]
    traindata = hindidata[:2000]+hindidata[3301:]

    testlabels = labels[2000:3000]
    validlabels = labels[3001:3300]
    trainlabels = labels[:2000]+labels[3301:]

    train=[[traindata],[trainlabels],[trainlabels]]
    test=[[testdata],[testlabels],[testlabels]]
    valid=[[validdata],[validlabels],[validlabels]]

    d={}
    d['words2idx']=hindidict
    d['labels2idx']=labelsdict
    d['tables2idx']=labelsdict
#    return [train,valid,test,d]
