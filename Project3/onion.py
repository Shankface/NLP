import numpy as np
import csv
from csv import reader
import random
import tensorflow as tf
from tensorflow import keras
from keras import layers
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, Dropout, Bidirectional, GlobalMaxPooling1D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential

from keras.utils import np_utils
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import pandas as pd


def rev(num):
    for i in tok_lists[num]:
        print(list(word_index.keys())[list(word_index.values()).index(i)])

def top(p,num):
    probs = p[0].tolist()
    top = []
    for _ in range(num):
        ind = np.argmax(probs)
        print(max(probs))
        top.append(ind)
        probs.pop(ind)
    print('')
    return random.choice(top)

texts = []

f = open("./OnionOrNot.csv")
csvreader = csv.reader(f)
header = next(csvreader)
for row in csvreader:
    if(row[1] == '0'):
        texts.append(row[0]+".")
    if(len(texts) == 8000):
      break
f.close()
#print(texts)

tokenizer = Tokenizer(oov_token = 'oov', filters = '*', split = ' ')
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index
n_words = len(word_index) + 1
print("# words: " + str(n_words))


input_seq = []
tok_lists = tokenizer.texts_to_sequences(texts)
for tok_list in tok_lists:
    #print(tok_list)
    for i in range(1,len(tok_list)):
        n_gram_seq = tok_list[:i+1]
        #print(n_gram_seq)
        input_seq.append(n_gram_seq)
        #if(i == 30):
        #    break

#print(sum([len(x) for x in tok_lists])/len(tok_lists))
max_seq_len = max([len(x) for x in input_seq])
input_seq = pad_sequences(input_seq, maxlen = max_seq_len, padding = 'pre')

inputs = input_seq[:,:-1]
labels = input_seq[:,-1]
y = np_utils.to_categorical(labels, num_classes = n_words)


# ----------- RNN ------------
#model = keras.Sequential()
#
#model.add(Embedding(input_dim = n_words, 
#                    output_dim = 240,
#                    input_length = max_seq_len-1))
#
#model.add(Bidirectional(LSTM(50)))
#
#model.add(Dense(n_words, activation = 'softmax'))
#adam = Adam(learning_rate = 0.01)
#model.compile(loss = 'categorical_crossentropy',
#                optimizer = adam,
#                metrics = ['accuracy'])
#model.summary()
#
#model.fit(inputs, y, epochs = 50)
#
#model.save('model2.h5')

model = keras.models.load_model('model2.h5')
#model.fit(inputs, y, batch_size = 256, epochs = 50)
seed = ''
while(True):

    seed = input("Input starting words: ")
    if(seed == "quit"):
        break

    while(True):
        token_list = tokenizer.texts_to_sequences([seed])
        token_list = pad_sequences(token_list, maxlen = max_seq_len-1, padding='pre')
        probs = model.predict(token_list)
        print(probs[0])
        print("sd: " + str(np.std(probs[0])))
        #ind = top_3(probs,2)
        top(probs,5)
        #print("max prob: " + str(max(probs[0])))
        #print("min prob: " + str(min(probs[0])))
        ind = np.argmax(probs)
        word = list(word_index.keys())[list(word_index.values()).index(ind)]
        seed += " " + word
        if(word[-1] == '.'):
            break

    print(seed+'\n')
