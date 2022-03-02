from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
#download("punkt")
download("stopwords")
from nltk.corpus import stopwords
from array import *
from collections import defaultdict
import math
from os.path import dirname
from random import randrange
import matplotlib.pyplot as plt

subjects = defaultdict(lambda : defaultdict(lambda: defaultdict(int))) # Holds each subject and its words and word probabilities
subjectData = defaultdict(lambda : defaultdict(int)) # Holds prob and count of each subject
totalFiles = 0

#print("Input Training Document:")
#train = input()
#print("Input Test Document:")
#test = input()
train = "./TC_provided/corpus3_train.labels"
test = "./TC_provided/corpus1_test.labels"

rando = []

stop_words = stopwords.words("english")

stop_words.extend([',', '.', '(', ')', '--', '"', "''", "'s", "n't", "``" ])

#print(stop_words)

# ---------------- Training ----------------
x = 0
with open(train) as f1:
    links = f1.readlines()
    #for link in links:
    for i in range(478):
        while(x in rando):
            x = randrange(0,955,1)
        rando.append(x)
        link = links[x]
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
                    #print(word)
                    if(subjects[subject][word]['wasCounted'] == False):
                        subjects[subject][word]['count'] += 1
                        subjects[subject][word]['wasCounted'] = True
                

for sub in subjectData:
    subjectData[sub]['prob'] = (subjectData[sub]['count'])/totalFiles
    print(sub + ": " + str(subjectData[sub]['prob']))
    
    for word in subjects[sub]:
        subjects[sub][word]['prob'] = (subjects[sub][word]['count'])/(subjectData[sub]['count'])



# ---------------- Testing ----------------
def alpha(prob, avg):
    
    if(prob > (avg/3)):
        return avg 
    return prob

guesses = defaultdict(int)
 # 0.05 for corp 1 and 2
K = len(subjectData)
avg = 1/K
A = []
b = 0.002
for x in range(100):
    A.append(b)
    b += .002
#print(A)

f = []
m = 0
ma = 0

print(len(rando))
for a in A:

    correct = 0
    with open(train) as f1:
        links = f1.readlines()
        #for link in links:
        for i in range(477):
            while(x in rando):
                x = randrange(0,955,1)
                print(x)
            rando.append(x)
            link = links[x]
            possible_sub = defaultdict(lambda: 0)

            s = dirname(train) + link.split()[0][1:]
            subj = link.split()[1]

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
                            possible_sub[sub] += math.log((c+a)/(N+(a*K)))

                            #    possible_sub[sub] += math.log(subjects[sub][word]['prob'])
                            #else:
                            #    possible_sub[sub] += math.log(alpha(subjectData[sub]['prob'], avg))
                guesses[link.split()[0]] = max(possible_sub, key = possible_sub.get)
                if(max(possible_sub, key = possible_sub.get) == subj):
                    correct += 1
            f2.close()
        f1.close()
    print(str(a) + ': ' + str(correct/477))
    if(correct/477 > m):
        m = correct/477
        ma = a
    f.append(correct/477)
print(max(f))
print(ma)
plt.plot(A,f)
plt.ylabel('some numbers')
plt.show()
plt.savefig("filename1.jpg")
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