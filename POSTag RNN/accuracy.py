import numpy
import pdb
import cPickle
import random

def conlleval(p, g, w, filename):
    '''
    INPUT:
    p :: predictions
    g :: groundtruth
    w :: corresponding words

    OUTPUT:
    filename :: name of the file where the predictions
    are written. it will be the input of conlleval.pl script
    for computing the performance in terms of precision
    recall and f1 score
    '''
    out = ''
    for sl, sp, sw in zip(g, p, w):
        out += 'BOS O O\n'
        for wl, wp, w in zip(sl, sp, sw):
            out += w + ' ' + wl + ' ' + wp + '\n'
        out += 'EOS O O\n\n'

    #f = open(filename,'w')
    #f.writelines(out)
    #f.close()
    correct=0
    wrong=0
    fp=open(filename)
    for i in fp:
        try:
            i=i.strip('\n').split(' ')
            act=i[1]
            pred=i[2]
            if act==pred:
                correct+=1
            else:
                wrong+=1
        except:
            continue
            
    ans= (float(correct)/float((correct+wrong)))*100
    print ans
    return {'p':ans, 'r':ans, 'f1':ans}     
  
