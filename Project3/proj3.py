import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
download("punkt")
download("stopwords")
from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname

train = "./TC_provided/corpus1_train.labels"
test = "./TC_provided/corpus1_test.labels"

subjects = defaultdict(lambda : defaultdict(int)) # Holds each subject and its words and word probabilities
word_counts = defaultdict(int)
all_words = []
train_sent = []
train_labels = []
test_sent = []
test_labels = []

def rev(num):
    for i in train_seq[num]:
        print(list(word_index.keys())[list(word_index.values()).index(i)])

with open(train) as f1:
    links = f1.readlines()

    for link in links:

        subject = link.split()[1]
        train_labels.append(subject)
        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            art = f2.read()
            words = word_tokenize(art)
            
            #all_words.append(words)
            train_sent.append(art)
            
            for word in words:     
                word_counts[word] += 1


with open(test) as f1:
    links = f1.readlines()

    for link in links:

        subject = link.split()[1]
        test_labels.append(subject)
        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            art = f2.read()
            words = word_tokenize(art)

            #all_words.append(words)
            test_sent.append(art)
            
print(train_labels)
word_count = len(word_counts)

tokenizer = Tokenizer(num_words = word_count)
tokenizer.fit_on_texts(train_sent)
word_index = tokenizer.word_index

train_seq = tokenizer.texts_to_sequences(train_sent)
train_pad = pad_sequences(train_seq, maxlen = 1000, padding = 'post', truncating = 'post')

test_seq = tokenizer.texts_to_sequences(test_sent)
test_pad = pad_sequences(test_seq, maxlen = 1000, padding = 'post', truncating = 'post')

## ----------- RNN ------------
model = keras.Sequential()

# Add an Embedding layer expecting input vocab of size word_counts, and
# output embedding dimension of size 64.
model.add(layers.Embedding(input_dim = word_count, 
                            output_dim = 64))

# Add a LSTM layer with 128 internal units.
model.add(layers.LSTM(128))

# Add a Dense layer with 10 units.
model.add(layers.Dense(5, activation = 'relu'))

model.summary()

