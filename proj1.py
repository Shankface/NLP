from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
download("punkt")
from array import *
from collections import defaultdict
import math


subjects = defaultdict(lambda : defaultdict(lambda: defaultdict(int)))
subjectData = defaultdict(lambda : defaultdict(int))
totalFiles = 0

with open("./TC_provided/corpus1_train.labels") as f1:
    links = f1.readlines()
    for link in links:

        subject = link.split()[1]
        subjectData[subject]['count'] += 1
        totalFiles += 1

        s = "./TC_provided" + link.split()[0][1:]

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
    
    for word in subjects[sub]:
        subjects[sub][word]['prob'] = (subjects[sub][word]['count'])/(subjectData[sub]['count'])
        




guesses = []

with open("./TC_provided/corpus1_test.list") as f1:
    links = f1.readlines()
    for link in links:
        possible_sub = defaultdict(lambda: 0)

        s = "./TC_provided" + link[1:-1]
        with open(s) as f2:
            words = word_tokenize(f2.read())
            for sub in subjects:
                possible_sub[sub] = math.log(subjectData[sub]['prob'])
                for word in words:
                    if(word.isalpha()):
                        if(word in subjects[sub]):
                            possible_sub[sub] += math.log(subjects[sub][word]['prob'])
                        else:
                            possible_sub[sub] += math.log(.00155)
            guesses.append(max(possible_sub, key = possible_sub.get))
        f2.close()


    f1.close()

    correct = 0

    with open("./TC_provided/corpus1_test.labels") as f1:
        links = f1.readlines()
        for i in range(443):
            if (links[i].split()[1] == guesses[i]):
                correct += 1

    print(correct/443)
