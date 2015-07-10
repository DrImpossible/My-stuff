from __future__ import absolute_import
from __future__ import print_function
import numpy as np
np.random.seed(1337) # for reproducibility
import gzip
import cPickle
from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU


'''
    Train a LSTM on the IMDB sentiment classification task.

    The dataset is actually too small for LSTM to be of any advantage 
    compared to simpler, much faster methods such as TF-IDF+LogReg.

    Notes: 

    - RNNs are tricky. Choice of batch size is important, 
    choice of loss and optimizer is critical, etc. 
    Some configurations won't converge.

    - LSTM loss decrease patterns during training can be quite different 
    from what you see with CNNs/MLPs/etc. 

    GPU command:
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python imdb_lstm.py
'''

max_features = 20000
maxlen = 30 # cut texts after this number of words (among top max_features most common words)
batch_size = 32
f = gzip.open('encodeddataset.pkl.gz', 'rb')
train_set, valid_set, test_set = cPickle.load(f)
print("Loading data...")
(X_train, y_train) = train_set 
(X_test, y_test) = test_set
print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

print("Pad sequences (samples x time)")
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128))
model.add(LSTM(128, 128)) # try using a GRU instead, for fun
model.add(Dropout(0.5))
model.add(Dense(128, 6))
model.add(Activation('softmax'))

# try using different optimizers and different optimizer configs
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

print("Train...")
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=4, validation_data=(X_test, y_test), show_accuracy=True)
score, acc = model.evaluate(X_test, y_test, batch_size=batch_size, show_accuracy=True)
print('Test score:', score)
print('Test accuracy:', acc)
