import re
import numpy as np
import sys,os

def matchPattern(s, l):
    for i,e in enumerate(l):
        if e in s:
            return i
    return -1

def executeForFile(inFile,outFile, total):
    doInclude = True
    toMatch = np.array([],dtype=str)
    depthCount = 0
    with open(inFile,"r") as inF, open(outFile,"w") as outF:
        for line in inF:
            if(toMatch.size != 0):
                i = matchPattern(line,toMatch)
                if( i == 1):
                    depthCount -= 1
                    if(depthCount == 0):
                        toMatch = np.array([],dtype=str)
                        if(not doInclude):
                            doInclude = True
                            continue
                elif(i == 0):
                    depthCount +=1
            else:
                i = matchPattern(line,total[:,0])
                if(i >= includes.shape[0]):
                    doInclude = False
                    depthCount = 1
                    toMatch = np.array(total[i])
                elif(i >= 0):
                    doInclude = True
                    depthCount = 1
                    toMatch = np.array(total[i])
            if(doInclude):
                outF.write(line)
                    

excludes = []
inStr = ""
outStr = ""
confStr = ""

if(len(sys.argv) != 4):
    print("Exactly 3 arguments are required: InDir OutDir Config")
    sys.exit()

inStr = sys.argv[1]
outStr = sys.argv[2]
confStr = sys.argv[3]        

with open(confStr,"r") as exF:
    for line in exF:
        entry = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
        entry = [e.replace("\"","") for e in entry]
        excludes.append(entry)

excludes = np.array(excludes) 
includes = np.array([['%ZFE begin include','%ZFE end include']])
total = np.vstack([includes,excludes])

inFiles = os.listdir(inStr)

R = re.compile(".*\.tex")
inFiles = list(filter(R.match,inFiles))

for fp in inFiles:
    executeForFile(os.path.join(inStr,fp),os.path.join(outStr,fp),total)
           

