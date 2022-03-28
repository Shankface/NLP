# NLP Projext 2
# Sentence Parser
# Ayden Shankman

from array import *
from collections import defaultdict
import sys

# ---------- Loading Grammar ----------
path = sys.argv[1]

print("Loading grammar...")
nonTerms = defaultdict(list)
Terms = defaultdict(list)

with open(path) as f:
    lines = f.readlines()

    for line in lines:
        A = line.split()[0]

        if len(line.split()) == 4:    
            B = line.split()[2]
            C = line.split()[3]
            nonTerms[B + " " + C].append(A)

        else:
            Terms[line.split()[2]].append(A)


# ---------- CKY Algorithm ----------
def CKY(s):
    numWords = len(s.split())

    table = [[[] for x in range(numWords)] for x in range(numWords)]

    for i in range(numWords):
        w = s.split()[i]
        for A in Terms[w]:
            table[i][i].append((A,(i,i,w,0),(i,i, w,0)))

    for i in range(1,numWords):
        for j in range(i,numWords):
            x = j-i
            y = j

            for k in range(i):
                x1 = x
                y1 = y - (i-k)

                x2 = x + k + 1
                y2 = y

                for n in range(len(table[x1][y1])):
                    for m in range(len(table[x2][y2])):
                    
                        a = table[x1][y1][n][0]
                        b = table[x2][y2][m][0]

                        if (a + " " + b) in nonTerms:
                            for item in nonTerms[a + " " + b]:
                                table[x][y].append(((item,(x1,y1,a,n),(x2,y2,b,m))))
    return table


# ---------- Parsing Algorithm ----------
def parse (x,y,z,tree, level = 1):
    term = table[x][y][z][0]
    pt = ''

    x1 = table[x][y][z][1][0]
    y1 = table[x][y][z][1][1]
    z1 = table[x][y][z][1][3]
    term1 = table[x][y][z][1][2]
    
    x2 = table[x][y][z][2][0]
    y2 = table[x][y][z][2][1]
    z2 = table[x][y][z][2][3]
    
    if(term1.islower()):
        return [("[" + term + " " + term1 + ']'),("[" + term + " " + term1 + ']')]

    p = '[' + term + " " + parse(x1,y1,z1,tree)[0] + " " + parse(x2,y2,z2,tree)[0] +  "]"
    
    if(tree == 'y'):
        pt = '[' + term + "\n" + '   '*level + parse(x1,y1,z1,tree,level+1)[1] + "\n" + '   '*level + parse(x2,y2,z2,tree,level+1)[1] + "\n" + '   '*(level-1)  + ']'

    return[p,pt]


# ---------- Inputting Sentences ----------
tree = input("Do you want textual parse trees to be displayed (y/n)?: ")
s = ''
while(s != 'quit'):
    s = input("Enter a sentence: ")
    if(s == 'quit'):
        print('Goodbye!')
        break

    x = 0
    table = CKY(s)
    numWords = len(s.split())
    valid = False

    for i in range(len(table[0][numWords-1])):
        if(table[0][numWords-1][i][0] == 'S'):
            if(not valid):
                print('VALID SENTENCE\n')
            x+=1
            print("Valid parse #" + str(x))
            t = parse(0,numWords-1,i,tree)
            print(t[0] + '\n' + t[1] + '\n')
    if(x == 0):
        print('NOT A VALID SENTENCE\n')
    else:
        print('Number of valid parses:',x,'\n')





        