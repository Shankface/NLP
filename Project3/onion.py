import numpy as np
import csv
from csv import reader

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

texts = [] # contains 15000 article titles

f = open("./OnionOrNot.csv")
csvreader = csv.reader(f)
header = next(csvreader)
for row in csvreader:
    if(row[1] == '0'):
        texts.append(row[0])
    if(len(texts)==5000):
        break
f.close()

tokenizer = Tokenizer(oov_token = 'oov')
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index
n_words = len(word_index) + 1  # 23000 words indexed
input_seq = []

tok_lists = tokenizer.texts_to_sequences(texts)

for tok_list in tok_lists:
    #print(tok_list)
    for i in range(1,len(tok_list)):
        n_gram_seq = tok_list[:i+1]
        #print(n_gram_seq)
        input_seq.append(n_gram_seq)
        if(i == 30):
            break


max_seq_len = max([len(x) for x in input_seq])
input_seq = pad_sequences(input_seq, maxlen = 30, padding = 'pre')

inputs = input_seq[:,:-1]
labels = input_seq[:,-1]
y = np_utils.to_categorical(labels, num_classes = n_words)


## ----------------- RNN ------------------
model = keras.Sequential()

# Add an Embedding layer expecting input vocab of size word_counts, and
# output embedding dimension of size 64.
model.add(Embedding(input_dim = n_words, 
                    output_dim = 240,
                    input_length = 30-1))

# Add a LSTM layer with 128 internal units.
model.add(LSTM(8))

# Add a Dense layer with 10 units.
model.add(Dense(n_words, activation = 'softmax'))

adam = Adam(learning_rate = 0.01)

model.compile(loss = 'categorical_crossentropy',
                optimizer = adam,
                metrics = ['accuracy'])

model.summary()

model.fit(inputs, y, epochs = 50, verbose = 1)

  