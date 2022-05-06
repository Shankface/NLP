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

## Function to print sentence based on tokenized sentence
def rev(tok_list):
    for i in tok_list:
        print(list(word_index.keys())[list(word_index.values()).index(i)])


## Get first 8000 Onion News Titles
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

## Tokenize words
tokenizer = Tokenizer(oov_token = 'oov', filters = '*', split = ' ')
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index
n_words = len(word_index) + 1
#print("# words: " + str(n_words))

## Tokenize all titles and split them based on preceding words
input_seq = []
tok_lists = tokenizer.texts_to_sequences(texts)
for tok_list in tok_lists:
    for i in range(1,len(tok_list)):
        n_gram_seq = tok_list[:i+1]
        input_seq.append(n_gram_seq)
        #if(i == 30):
        #    break

max_seq_len = max([len(x) for x in input_seq])
input_seq = pad_sequences(input_seq, maxlen = max_seq_len, padding = 'pre') # make sure all input sentences are same length with padding 

## Split data into inputs and labels
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
#model.summary()
#model.fit(inputs, y, batch_size = 256, epochs = 50)
#model.save('model3.h5')

## 
seed = ''
while(True):

    seed = input("Input starting words: ")
    if(seed == "quit"):
        break

    while(True):
        token_list = tokenizer.texts_to_sequences([seed])
        token_list = pad_sequences(token_list, maxlen = max_seq_len-1, padding='pre')

        probs = model.predict(token_list)

        probs = probs[0][1:]

        ind = random.choices(list(word_index.values()), weights = probs, k = 100)
        ind = random.choice(ind)
        #ind = np.argmax(probs[0])
        word = list(word_index.keys())[list(word_index.values()).index(ind)]
        seed += " " + word
        if(word[-1] == '.'):
            break

    print("New Onion Article:\n" + seed +'\n')
