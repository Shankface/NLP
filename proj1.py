from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
#download("punkt")
#download("stopwords")
#from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname
#stop_words = set(stopwords.words("english"))
from random import randrange

subjects = defaultdict(lambda : defaultdict(lambda: defaultdict(int))) # Holds each subject and its words and word probabilities
subjectData = defaultdict(lambda : defaultdict(int)) # Holds prob and count of each subject
totalFiles = 0

#print("Input Training Document:")
#train = input()
#print("Input Test Document:")
#test = input()
train = "./TC_provided/corpus1_train.labels"
test = "./TC_provided/corpus1_test.list"

# ---------------- Training ----------------

with open(train) as f1:
    links = f1.readlines()
    for link in links:
  
        subject = link.split()[1]
        subjectData[subject]['count'] += 1
        totalFiles += 1

        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            
            words = word_tokenize(f2.read())

            for word in subjects[subject]:
                subjects[subject][word]['wasCounted'] = False

            for word in words:
                if(word.isalpha()):
                    if(subjects[subject][word]['wasCounted'] == False):
                        subjects[subject][word]['count'] += 1
                        subjects[subject][word]['wasCounted'] = True

for sub in subjectData:
    subjectData[sub]['prob'] = (subjectData[sub]['count'])/totalFiles
    
    #for word in subjects[sub]:
    #    subjects[sub][word]['prob'] = (subjects[sub][word]['count'])/(subjectData[sub]['count'])


# ---------------- Testing ----------------

guesses = defaultdict(int)
a = .1 # 0.05 for corp 1 and 2
K = len(subjectData)

with open(test) as f1:
    links = f1.readlines()
    for link in links:
    
        possible_sub = defaultdict(lambda: 0)
        
        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            words = word_tokenize(f2.read())
            
            for sub in subjects:
                possible_sub[sub] = math.log(subjectData[sub]['prob'])

                for word in words:
                    if(word.isalpha()):
                        c = 0
                        if(word in subjects[sub]):
                            c = subjects[sub][word]['count']
                        N = subjectData[sub]['count']
                        
                        possible_sub[sub] += math.log((c+a)/(N+(a*K)))
                        #if(word in subjects[sub]):
                        #    possible_sub[sub] += math.log(subjects[sub][word]['prob'])
                        #else:
                        #    possible_sub[sub] += math.log(.00155)

            guesses[link.split()[0]] = max(possible_sub, key = possible_sub.get)
            #if(max(possible_sub, key = possible_sub.get) == subj):
            #    correct += 1
        f2.close()
    f1.close()

#with open("./TC_provided/corpus1_test.labels") as f:
#    links = f.readlines()
#    for link in links:
#        if(guesses[link.split()[0]] == link.split()[1]):
#            correct += 1
#    f.close()
#
#print(correct/len(guesses))


print("Input Output Document:")
out = input()

f = open(out, "w")
for guess in guesses:
    f.write(guess + " " + str(guesses[guess]) + '\n')
f.close()