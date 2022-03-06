from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
download("punkt")
download("stopwords")
from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname
from random import *
import matplotlib.pyplot as plt

avg = []
avgm = []
alp = defaultdict(int)

print("trial: " + str(i))
subjects = defaultdict(lambda : defaultdict(int)) # Holds each subject and its words and word probabilities
subjectData = defaultdict(lambda : defaultdict(int)) # Holds prob and count of each subject
totalFiles = 0

print("Input Training Document:")
train = input()
print("Input Test Document:")
test = input()
#train = "./TC_provided/corpus2_train.labels"
#test = "./TC_provided/corpus1_test.labels"

stop_words = stopwords.words("english")

# ---------------- Training ----------------
with open(train) as f1:
    links = f1.readlines()

    for link in links:
    
        subject = link.split()[1]
        subjectData[subject]['count'] += 1
        totalFiles += 1

        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            seen_words = []
            words = word_tokenize(f2.read())

            #for word in subjects[subject]:
               # subjects[subject][word]['wasCounted'] = False

            for word in words:
                if((word.isalpha()) and (word not in stop_words) and (word not in seen_words)):
                    subjects[subject][word] += 1
                    seen_words.append(word)
                    #all_words[word] += 0
                    #if(subjects[subject][word]['wasCounted'] == False):
                        #subjects[subject][word]['count'] += 1
                        #subjects[subject][word]['wasCounted'] = True

for sub in subjectData:
    subjectData[sub]['prob'] = (subjectData[sub]['count'])/totalFiles


# ---------------- Testing ----------------

guesses = defaultdict(int)
K = len(subjectData)

a = .0155

for n in range(1):
    #a += .0005
    correct = 0
    with open(train) as f1:
        links = f1.readlines()
        #for link in links:
        for x in range(750, 894):
            link = links[r[x]]
            possible_sub = defaultdict(lambda: 0)
            s = dirname(train) + link.split()[0][1:]
            subj = link.split()[1]
            with open(s) as f2:
                words = word_tokenize(f2.read())
                for sub in subjects:
                    possible_sub[sub] = math.log(subjectData[sub]['prob'])
                    N = subjectData[sub]['count']
                    for word in words:
                        if((word.isalpha())and (word not in stop_words)):
                            c = 0
                            if(word in subjects[sub]):
                                c = subjects[sub][word]
                            possible_sub[sub] += math.log((c+a)/(N+(a*K)))
                guesses[link.split()[0]] = max(possible_sub, key = possible_sub.get)
                if(max(possible_sub, key = possible_sub.get) == subj):
                    correct += 1
            f2.close()
    f1.close()

print("Input Output Document:")
out = input()

f = open(out, "w")
for guess in guesses:
    f.write(guess + " " + str(guesses[guess]) + '\n')
f.close()