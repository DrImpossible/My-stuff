import spell
from nltk.corpus import wordnet as wn

spellchecked=''
inp=raw_input('Enter the question.')
inp=inp.lower()
print inp
inp=inp.strip('\n').split(' ')

for i in inp:
    spellchecked+=(spell.correct(i)+' ')
    
spellchecked=spellchecked.strip(' ').split(' ')
print spellchecked

for i in xrange(len(spellchecked)):
    syn=wn.synsets(spellchecked[i])
    for j in xrange(len(syn)):
        syn[j]=str(syn[j]).split('\'')[1].split('.')[0]
    b=set(syn)
    print b
    

