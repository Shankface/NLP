
from array import *
from collections import defaultdict
import sys

#path = sys.argv[1]

print("Loading grammar...")
nonTerms = defaultdict(list)
Terms = defaultdict(list)

with open('cnf.txt') as f:
    lines = f.readlines()

    for line in lines:
        A = line.split()[0]

        if len(line.split()) == 4:    
            B = line.split()[2]
            C = line.split()[3]
            nonTerms[B + " " + C].append(A)

        else:
            Terms[line.split()[2]].append(A)

s = 'i book the flight to houston'
numWords = len(s.split())

table = [[[] for x in range(numWords)] for x in range(numWords)]

for i in range(numWords):
    w = s.split()[i]
    for A in Terms[w]:
        table[i][i].append((A,(i,i,w,0),(i,i, w,0)))

#for n in range(numWords):
#    for m in range(numWords):
#        print(table[n][m], end= " ")
#    print('\n')

for i in range(1,numWords):
    for j in range(i,numWords):
        x = j-i
        y = j

        #print("box = " + str(x) + "," + str(y))

        for k in range(i):
            x1 = x
            y1 = y - (i-k)
            
            x2 = x + k + 1
            y2 = y

            #print("current = " + str(x1) + "," + str(y1) + " -> " + str(x2) + "," + str(y2))

            for n in range(len(table[x1][y1])):
                for m in range(len(table[x2][y2])):
    
                    a = table[x1][y1][n][0]
                    b = table[x2][y2][m][0]
                    #print(a,b)
                    if (a + " " + b) in nonTerms:
                        #print("Match: " + a + ' ' + b + ' -> ' + str(nonTerms[a + " " + b]))

                        for item in nonTerms[a + " " + b]:
                            table[x][y].append(((item,(x1,y1,a,n),(x2,y2,b,m))))

                        
                        #for n in range(numWords):
                        #    for m in range(numWords):
                        #        print(table[n][m], end= " ")
                        #    print('\n')

#for i in range(numWords):
#    for j in range(numWords):
#        print(i,j,end = " ")
#        print(table[i][j])
#    print('\n')


def parse (x,y,z):
    t = table[x][y][z][0]

    x1 = table[x][y][z][1][0]
    y1 = table[x][y][z][1][1]
    z1 = table[x][y][z][1][3]
    term1 = table[x][y][z][1][2]
    
    x2 = table[x][y][z][2][0]
    y2 = table[x][y][z][2][1]
    z2 = table[x][y][z][2][3]
    
    if(term1.islower()):
        return "[" + t + " " + term1 + ']'
    return '[' + t + " " + parse(x1,y1,z1) + " " + parse(x2,y2,z2) +  "]"

def parseTree (x,y,z,level = 1):
    t = table[x][y][z][0]

    x1 = table[x][y][z][1][0]
    y1 = table[x][y][z][1][1]
    z1 = table[x][y][z][1][3]
    term1 = table[x][y][z][1][2]
    
    x2 = table[x][y][z][2][0]
    y2 = table[x][y][z][2][1]
    z2 = table[x][y][z][2][3]

    if(term1.islower()):
        return "[" + t + " " + term1 + ']'
    s = '[' + t + '\n' + '   '*level + parseTree(x1,y1,z1,level+1) + '\n' + '   '*level + parseTree(x2,y2,z2,level+1) + '\n' + '   '*(level-1)  + ']'
    return s 

x = 1
for i in range(len(table[0][numWords-1])):
    if(table[0][numWords-1][i][0] == 'S'):
        print("Valid parse #" + str(x))
        print(parse(0,numWords-1,i),'\n')
        print(parseTree(0,numWords-1,i),'\n')
        x+=1