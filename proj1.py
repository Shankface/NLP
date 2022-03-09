from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
download("punkt")
download("stopwords")
from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname

subjects = defaultdict(lambda : defaultdict(int)) # Holds each subject along with each the count of how many documents each word appears per subject
subjectData = defaultdict(lambda : defaultdict(int)) # Holds probability and document count for each subject
totalFiles = 0

print("Input Training Document:")
train = input()
print("Input Test Document:")
test = input()
#train = "./TC_provided/corpus1_train.labels"
#test = "./TC_provided/corpus1_test.labels"

stop_words = stopwords.words("english")

# ---------------- Training ----------------

with open(train) as f1:
    lines = f1.readlines()

    for line in lines:
    
        subject = line.split()[1]
        subjectData[subject]['count'] += 1
        totalFiles += 1

        path = dirname(train) + line.split()[0][1:] # article path

        with open(path) as f2:
            seen_words = []
            words = word_tokenize(f2.read())

            for word in words:
                if((word.isalpha()) and (word not in stop_words) and (word not in seen_words)):
                    subjects[subject][word] += 1
                    seen_words.append(word)

for sub in subjectData:
    subjectData[sub]['prob'] = (subjectData[sub]['count'])/totalFiles



# ---------------- Testing ----------------

guesses = defaultdict(int)
K = len(subjectData)

#smoothing factor
if(K == 5): # Corpus1
    a = .095
if(K == 2): # Corpus1
    a = .0155
if(K == 6): # Corpus1
    a = .06

with open(test) as f1:

    lines = f1.readlines()

    for line in lines:

        possible_sub = defaultdict(lambda: 0)
        path = dirname(train) + line.split()[0][1:]

        with open(path) as f2:
            words = word_tokenize(f2.read())

            for sub in subjects:
                
                possible_sub[sub] = math.log(subjectData[sub]['prob']) # add probabilty of subject
                N = subjectData[sub]['count']
                
                for word in words:
                    
                    if((word.isalpha()) and (word not in stop_words)):
                        c = 0

                        if(word in subjects[sub]): 
                            c = subjects[sub][word] # number of documents in certain subject that word appears

                        possible_sub[sub] += math.log((c+a)/(N+(a*K))) # probability that word is in subject with smoothing factor
 
            guesses[line.split()[0]] = max(possible_sub, key = possible_sub.get)
            
        f2.close()
f1.close()


# ------------- Writing to Output File -------------

print("Input Output Document:")
out = input()

f = open(out, "w")
for guess in guesses:
    f.write(guess + " " + str(guesses[guess]) + '\n')
f.close()