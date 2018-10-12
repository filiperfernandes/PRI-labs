import re, nltk, sys


token = sys.argv[1]
docs = ("d1.txt", "d2.txt", "d3.txt", "d4.txt")

#f = open("files.txt", "r")
#print(f.read())
cnt = nltk.Counter()

dict= {}
listWords=[]
fileList=[]
i=0
with open("files.txt") as f:
    for line in f:
        print(line)
        f = open(line.rstrip('\n'), "r")
        raw = f.read()
        fileList.append(raw)
        raw2 = re.split("\W+", raw)
        listWords.append(raw2)
        for word in raw2:
            cnt[word] += 1

for el in fileList:
    cnt2 = nltk.Counter()
    raw3 = re.split("\W+", el)
    i=i+1
    for word2 in raw3:
        cnt2[word2] += 1
    dict[i] = cnt2

print(cnt)
print(fileList)

print(dict)
print(dict[1][token])
print(dict[2][token])
print(dict[3][token])
print(dict[4][token])
        #print(f.read())
        #dict[line.rstrip('\n')] = f.
#print(dict)
