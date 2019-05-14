# -*- coding: utf-8 -*-
"""

@author: Accacio
"""

import math
import sys
import csv
import functools
import itertools

class Record: 
    def __init__(self,seq,ioVector,ioNames):
        self.seq = seq
        self.ioVec = ioVector
        self.ioNames = ioNames


    def __str__(self):
        return str(self.seq) + "," + str(self.ioVec)+ "," + str(self.ioNames)

        
    def copyRecord(self):
        return Record(self.seq,self.ioVec,self.ioNames)



class MyUtil:
    def __init__(self,verbose,debug):
        self.debug=debug
        self.verbose=verbose

    def printv(self,string):
        if self.verbose==True:
            for i in string:
                print(i, end='')
            print("")

    def printdnl(self,*string,end=''):
        if self.debug==True:
            for i in string:
                print(i,end='')

    def printd(self,*string,end=''):
        if self.debug==True:
            for i in string:
                print(i,end='')            
            print()

class TableReader(MyUtil):
    def __init__(self,files,verbose,debug):
        MyUtil.__init__(self,verbose,debug)
        self.files = files

    def getRecordFromFile(self):
        self.printd("<<==Reading Table - BEGIN ==>>")
        readers=[]
        for file in self.files:
            readers.append(csv.DictReader(file,delimiter=','))

        records=[]
        # todo test number of collumns
        for reader in readers:
            lineCount=0
            collumnNames=[]
            for row in reader:
                if lineCount==0:
                    for collumn in row:
                        collumnNames.append(collumn)
                    # self.printd("Collumn Names: \n",collumnNames)
                    
                if row[collumnNames[0]]!="//END":
                    # print(row[collumnNames[1]])
                    listItems=list(row.items())
                    ioVector=list(map(lambda x : x[1],listItems[1:len(row)]))
                    ioVector=functools.reduce(lambda x,y: str(x) + str(y),ioVector)
                    newRecord=Record(row[collumnNames[0]],ioVector,collumnNames[1:])
                    self.printd(newRecord)
                    records.append(newRecord)

                lineCount+=1

        self.printd("<<==Reading Table - END ==>>")
        return records

class PathManager(MyUtil):
    def __init__(self,records,verbose,debug):
        MyUtil.__init__(self,verbose,debug)
        self.records = records
        self.paths=self.getPathsFromRecord()
        

    def printPathd(self,paths):
        if self.debug==True:
            for path in paths:
                print("Path",paths.index(path))
                if isinstance(path,list):
                    for i in path:
                        print(i.ioVec,"",end="")
                else:
                    print(p)
                print()

    def printModifiedPathsd(self,paths):
        if self.debug==True:
            for path in paths:
                print("Path",paths.index(path))
                if isinstance(path,list):
                    for i in path:
                        for j in i:
                            print(j.ioVec,"")
                        print()
                else:
                    print(p)
                print()


    def getPaths(self):
        return self.paths

    def getModifiedPaths(self,k):
        self.printd("<<==Getting Modified Paths from Paths - BEGIN ==>>")



        # def getEvent(self,vecin,vecout):
        #     N = table_read.ioVectorLength
        #     event = ''
        #     for i in range(len(vecin)):
        #         if vecin[i]!=vecout[i]:
        #         kvector = '0'*i+'1'+'0'*(N-i-1)
        #         e = IO.tagger(kvector)[0]
        #         #e = str(i)
        #         if vecin[i]=='0': 
        #             event = event + e + '_1 '
        #         else: event = event + e + '_0 '
        # if event=='': return 'Equal vectors!'
        # return event                     


        sigma=[]
        modifiedPaths=[]
        for path in self.paths:
            newpath = []
            newSigma = []
            l = len(path)
            self.printd("Path ",self.paths.index(path))
            for j in range(l):
                if j<=l-1:
                    if k<=j+1:
                        newVector = path[j-k+1:j+1]
                    
                    elif j+1<k:
                        newVector = path[:j+1]

                    if j<l-1:
                        newSigma = self.getSigma(path[j],path[j+1])

                newpath.append(newVector)
                
                for i in newVector:
                    self.printd(i.ioVec)
                self.printd()

                
                
                
            modifiedPaths.append(newpath)
        self.printd("<<==Getting Modified Paths from Paths - END ==>>")            
        return (modifiedPaths, sigma)

    def getSigma(self,record,recordPrime):
        vec=record.ioVec
        vecPrime=recordPrime.ioVec
        names=record.ioNames
        self.printd(record.ioVec," -> ",recordPrime.ioVec)
        self.printd()
        diff=[i for i in range(len(vec)) if vec[i] != vecPrime[i]]

        for i in diff:
            self.printdnl(names[i])
            if vec[i]=='0' and vecPrime[i]=='1':
                self.printdnl("^ ")
            if vec[i]=='1' and vecPrime[i]=='0':
                self.printdnl("v ")
        self.printd()
        
        # for i in record.ioVec:
        #     self.printd(i,recordPrime.ioVec[int(i)])
        
        # return
    
    def getPathsFromRecord(self):
        self.printd("<<==Getting Paths from Record - BEGIN ==>>")
        paths=[]

        #Exclude the neighbours vectors that are equal
        newRecord=self.records[0]
        newRecords = [newRecord]
        self.printd(newRecord)
        for i in range(len(self.records) - 1):
            if self.records[i].ioVec!=self.records[i+1].ioVec or \
               self.records[i].ioVec==self.records[0].ioVec:
                newRecord=self.records[i+1]
                self.printd(newRecord)
                newRecords.append(self.records[i+1])
            else:
                self.printd(self.records[i+1]," ==> Removed")

        self.printd("===== Nodes selected as beginning of paths")
        #Find the vectors that are equal to the first one to separate the paths
        pathsBeginInd = [0]
        self.printd(newRecords[0], " *")
        for i in range(1,len(newRecords)):
            if newRecords[0].ioVec==newRecords[i].ioVec:
                self.printd(newRecords[i]," *")
                pathsBeginInd.append(i)
            else:
                self.printd(newRecords[i])
        self.printd(pathsBeginInd)

        #Obtain the candidates to paths
        self.printd("==== Path candidates")
        P = []
        for i in range(len(pathsBeginInd)):
            path=[]
            if i == len(pathsBeginInd)-1:
                path=newRecords[pathsBeginInd[i]:]
            else:
                path=newRecords[pathsBeginInd[i]:pathsBeginInd[i+1]+1]
            self.printd("path ", i)
            for p in path:
                self.printdnl(p.ioVec," ")
            self.printd("")
            self.printd("end")
            P.append(path)

        self.printd("==== Removing superposed")
        pathsNoSuper=P.copy()
        for i in pathsNoSuper:
            for j in pathsNoSuper:
                if i!=j:

                    ioVeci = [rec.ioVec for rec in i]
                    ioVecj = [rec.ioVec for rec in j]

                    if ioVecj==ioVeci[:len(ioVecj)]:
                        # self.printdnl("Path ", pathsNoSuper.index(i), " includes path ", pathsNoSuper.index(j))
                        # self.printd(" -> removing path ", pathsNoSuper.index(j))
                        pathsNoSuper.remove(j)
            
        self.printPathd(pathsNoSuper)

        # self.printd("==== Removing superposed Met-0")
        # for i in range(len(P)):
        #     for j in range(len(P)):
        #         if i!=j and P[i]!=0 and P[j]!=0:
        #             ioVeci = [rec.ioVec for rec in P[i]]
        #             ioVecj = [rec.ioVec for rec in P[j]]
        #             if ioVecj==ioVeci[:len(ioVecj)]:
        #                 self.printdnl("Path ", i, " includes path ",j)
        #                 self.printd(" -> removing path ",j)
        #                 P[j]=0
                    
        # i = 0
        # while i < len(P):
        #     if P[i]==0:
        #         del P[i]
        #     else:
        #         i+=1
        # self.printPathd(P)

        #Eliminate paths formed by two elements where both are the initial state                    
        self.printd("==== Removing 2 node circular path")
        # pathsNoTwoElemCircPath=pathsNoSuper.copy()
        # for i in pathsNoTwoElemCircPath:
        #     if i[0].ioVec == i[1].ioVec:
        #         pathsNoTwoElemCircPath.remove(i)
        pathsNoTwoElemCircPath=list(filter(lambda x: x[0].ioVec!=x[1].ioVec,pathsNoSuper))

        self.printPathd(pathsNoTwoElemCircPath)
        
        # #Eliminate paths formed by two elements where both are the initial state                    
        # self.printd("==== Removing 2 node circular path - Met 0")
        # for i in range(len(P)):
        #     if isinstance(P[i],list):
        #         if P[i][0].ioVec == P[i][1].ioVec:
        #             P[i] = 0

        # i = 0
        # while i < len(P):
        #     if P[i]==0:
        #         del P[i]
        #     else:
        #         i+=1

        # self.printPathd(P)

        paths = pathsNoTwoElemCircPath
        self.printd("<<==Getting Paths from Record - END ==>>")
        return paths

    

