#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import getopt
import utils as ut

# config variables
version=0.0
inputFiles=[]
outputFile=""
verbose=False
graphviz=False
fromStdin=False
debug=False
paramk=1


def usage():
    print("Usage: daoct [OPTION]")
    return 

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:],"k:shgi:o:",["input=","output=","verbose","graphviz","debug","version","paramk="])
except getopt.GetoptError:
    usage()
    sys.exit(-1)

if opts==[] or opts==[('--debug','')]or opts in [('--verbose','')]:
    usage()
    sys.exit(-1)


files=[]
for opt, arg in opts:
    if opt in ("-h","--help"):
        usage()
        sys.exit()
    if opt in ("--version"):
        print("VERSION:",version)
        sys.exit()
    if opt in ("--verbose"):
        verbose=True
    if opt in ("-g","--graphviz"):
        graphviz=True
    if opt in ("-k"):
        paramk=int(arg)
    if opt in ("--debug"):
        debug=True
    if opt in ("-i", "--input"):
        inputFiles.append(arg)
    if opt in ("-s", "--stdin"):
        fromStdin=True
    if opt in ("-o", "--output"):
        outputFile=arg

myutil = ut.MyUtil(verbose,debug)    
if inputFiles==[] and fromStdin==True:
    try:
        files.append(sys.stdin.readlines())
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.exit(-1)
elif inputFiles!=[]:
    try:
        for inputFile in inputFiles:
            files.append(open(inputFile,newline=''))
        # filedata=file.read()
    except FileNotFoundError:
        print("File not Found, please insert a valid file name")
        sys.exit(-1)
else:
    usage()
    sys.exit(-1)
    


myutil.printd("VERSION          :",version)
myutil.printd("ARGUMENTS        :",sys.argv[:])
myutil.printd("OPTS             :",opts)
myutil.printd("ARGS             :",args)
myutil.printd("VERBOSE          :",verbose)
myutil.printd("GRAPHVIZ         :",graphviz)
myutil.printd("INPUTFILES       :",inputFiles)
myutil.printd("OUTPUT FILE NAME :",outputFile)
myutil.printd("PARAMETER k      :",paramk)

myTR = ut.TableReader(files,verbose,debug)
records = myTR.getRecordFromFile()
myPM = ut.PathManager(records,verbose,debug)
paths = myPM.getPaths()
modifiedPaths, modifiedSigmas = myPM.getModifiedPaths(paramk)

print("original")
myPM.printPathd(paths)
print("modified")
myPM.printModifiedPathd(modifiedPaths)

