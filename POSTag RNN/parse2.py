def fuckyou():
#if 1==1: 
    fp=open('news_wx')
    
    hindidata=[]
    labels=[]
        
    for i in fp:
        j=i.strip('\n').split(' ')
        for k in j:
            word=k.split('\\')
            if word[1]!='.':
                hindidata.append(word[0])
                labels.append(word[1])
        
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
            print i
       
    print len(hindidata)
    print len(labels)
    
    for i in xrange(len(hindidata)):
        hindidata[i]=hindidict[hindidata[i]]
        
    for i in xrange(len(labels)):
        labels[i]=labelsdict[labels[i]]
           
    #print hindidata[0:10]
    #print labels[0:10]

    testdata = hindidata[0:23365]
    validdata = hindidata[23366:30000]
    traindata = hindidata[30001:]

    testlabels = labels[0:23365]
    validlabels = labels[23366:30000]
    trainlabels = labels[30001:]

    train=[[traindata],[trainlabels],[trainlabels]]
    test=[[testdata],[testlabels],[testlabels]]
    valid=[[validdata],[validlabels],[validlabels]]
    
    d={}
    d['words2idx']=hindidict
    d['labels2idx']=labelsdict
    d['tables2idx']=labelsdict
    return [train,valid,test,d]
