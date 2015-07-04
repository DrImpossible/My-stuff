import nltk
from nltk.corpus import wordnet as wn

question=raw_input('Test: Type a question?\n')

tokens=nltk.word_tokenize(question)
tagged=nltk.pos_tag(tokens)
chunked=nltk.chunk.ne_chunk(tagged)

spellchecked=question.strip('\n').split(' ')
for i in xrange(len(spellchecked)):
    syn=wn.synsets(spellchecked[i])
    for j in xrange(len(syn)):
        syn[j]=str(syn[j]).split('\'')[1].split('.')[0]
    b=set(syn)
    if tagged[i][1][0]=='N' or tagged[i][1][0]=='V':
        print b
print question
print tokens
print tagged
print chunked

