#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import getopt
import utils as ut

# config variables
version=0.0
inputFile=""
outputFile=""
verbose=False
graphviz=False
debug=False



def usage():
    print("Usage: daoct [OPTION]")
    return 

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:],"shgi:o:",["input=","output=","verbose","graphviz","debug","version"])
except getopt.GetoptError:
    usage()
    sys.exit(-1)

if opts==[] or opts==[('--debug','')]or opts in [('--verbose','')]:
    usage()
    sys.exit(-1)


file=""
for opt, arg in opts:
    if opt in ("-h","--help"):
        usage()
        sys.exit()
    if opt in ("","--version"):
        print("VERSION:",version)
        sys.exit()
    if opt in ("--verbose"):
        verbose=True
    if opt in ("-g","--graphviz"):
        graphviz=True
    if opt in ("--debug"):
        debug=True
    if opt in ("-i", "--input"):
        inputFile=arg
    if opt in ("-s", "--stdin"):
        fromStdin=True
    if opt in ("-o", "--output"):
        outputFile=arg

myutil = ut.MyUtil(verbose,debug)    
if inputFile=="" and fromStdin==True:
    try:
        file=sys.stdin.readlines()
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.exit(-1)
elif inputFile!="":
    try:
        file=open(inputFile,newline='')
        # filedata=file.read()
    except FileNotFoundError:
        print("File not Found, please insert a valid file name")
        sys.exit(-1)
else:
    usage()
    


myutil.printd("VERSION          :",version)
myutil.printd("ARGUMENTS        :",sys.argv[:])
myutil.printd("OPTS             :",opts)
myutil.printd("ARGS             :",args)
myutil.printd("VERBOSE          :",verbose)
myutil.printd("GRAPHVIZ         :",graphviz)
myutil.printd("INPUTFILE        :",inputFile)
myutil.printd("OUTPUT FILE NAME :",outputFile)
# myutil.printd("PATH SIZE        :","\n",file.read())

myTR= ut.TableReader(file,verbose,debug)
data, collumns = myTR.readTable()
print(collumns)
