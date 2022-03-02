from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
#download("punkt")
#download("stopwords")
#from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname
from random import *
import matplotlib.pyplot as plt

subjects = defaultdict(lambda : defaultdict(lambda: defaultdict(int))) # Holds each subject and its words and word probabilities
subjectData = defaultdict(lambda : defaultdict(int)) # Holds prob and count of each subject
totalFiles = 0
all_words = defaultdict(int)

#print("Input Training Document:")
#train = input()
#print("Input Test Document:")
#test = input()
train = "./TC_provided/corpus1_train.labels"
test = "./TC_provided/corpus1_test.list"

#stop_words = stopwords.words("english")

#stop_words.extend([',', '.', '(', ')', '--', '"', "''", "'s", "n't", "``" ])

#print(stop_words)
#r = sample(range(954), 954)

# ---------------- Training ----------------
x = 0
with open(train) as f1:
    links = f1.readlines()
    for link in links:
    #for i in range(478):
        #link = links[r[i]]
        subject = link.split()[1]
        subjectData[subject]['count'] += 1
        totalFiles += 1

        s = dirname(train) + link.split()[0][1:]

        with open(s) as f2:
            
            words = word_tokenize(f2.read())

            for word in subjects[subject]:
                subjects[subject][word]['wasCounted'] = False

            for word in words:
                #if((word not in stop_words) and (not word.isdigit())):
                if(word.isalpha()):
                    all_words[word] += 0
                    if(subjects[subject][word]['wasCounted'] == False):
                        subjects[subject][word]['count'] += 1
                        subjects[subject][word]['wasCounted'] = True
                
for sub in subjectData:
    subjectData[sub]['prob'] = (subjectData[sub]['count'])/totalFiles
    #print(sub + ": " + str(subjectData[sub]['prob']))
    
    #for word in subjects[sub]:
    #    subjects[sub][word]['prob'] = (subjects[sub][word]['count'])/(subjectData[sub]['count'])



# ---------------- Testing ----------------

guesses = defaultdict(int)

K = len(all_words)
A = [.005]
#b = .01
#for x in range(1):
#    A.append(b)
#    b += .01

f = []
m = 0
ma = 0

for a in A:
    #correct = 0
    print(a)
    with open(test) as f1:
        links = f1.readlines()
        for link in links:
        #for i in range(478,954):
            #link = links[r[i]]
            possible_sub = defaultdict(lambda: 0)

            s = dirname(train) + link.split()[0][1:]
            #subj = link.split()[1]

            with open(s) as f2:
                words = word_tokenize(f2.read())

                for sub in subjects:
                    possible_sub[sub] = math.log(subjectData[sub]['prob'])
                    N = subjectData[sub]['count']

                    for word in words:
                        #if((word not in stop_words) and (not word.isdigit())):
                        if(word.isalpha()):
                            c = 0
                            if(word in subjects[sub]):
                                #a = 0
                                c = subjects[sub][word]['count']
                            #print((c+a)/N)
                            possible_sub[sub] += math.log((c+a)/(N+(a*K)))#+(.03*K)))

                            #    possible_sub[sub] += math.log(subjects[sub][word]['prob'])
                            #else:
                            #    possible_sub[sub] += math.log(alpha(subjectData[sub]['prob'], avg))
                guesses[link.split()[0]] = max(possible_sub, key = possible_sub.get)
                #if(max(possible_sub, key = possible_sub.get) == subj):
                    #correct += 1
            f2.close()
        f1.close()
    #print(str(a) + ': ' + str(correct/len(guesses)))
    #if(correct/len(guesses) > m):
    #    m = correct/len(guesses)
    #    ma = a
    #f.append(correct/len(guesses))
    break
#print(max(f))
#print(ma)

#plt.plot(A,f)
#plt.ylabel('some numbers')
#plt.show()
#plt.savefig("filename2.jpg")
correct = 0
with open("./TC_provided/corpus1_test.labels") as f:
    links = f.readlines()
    for link in links:
        if(guesses[link.split()[0]] == link.split()[1]):
            correct += 1
    f.close()

print(correct/len(guesses))


print("Input Output Document:")
out = input()

f = open(out, "w")
for guess in guesses:
    f.write(guess + " " + str(guesses[guess]) + '\n')
f.close()