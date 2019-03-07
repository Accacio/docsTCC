import math
import sys
import csv
import functools

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
                    print(newRecord)
                    records.append(newRecord)

                lineCount+=1

        self.printd("<<==Reading Table - END ==>>")
        return records

class PathManager(MyUtil):
    def __init__(self,records,verbose,debug):
        MyUtil.__init__(self,verbose,debug)
        self.records = records
        
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
                self.printdnl(p.ioVec)
            self.printd("")
            self.printd("end")
            P.append(path)

        self.printd("==== Remove superposed")
        pathNoSuper=[]
        for i in range(len(P)):
            for j in range(len(P)):
                if i!=j and P[i]!=0 and P[j]!=0:

                    ioVeci = [rec.ioVec for rec in P[i]]
                    ioVecj = [rec.ioVec for rec in P[j]]
                    if ioVecj==ioVeci[:len(ioVecj)]:
                        self.printdnl("Path ", i, " includes path ",j)
                        self.printd(" -> removing path ",j)
                        P[j]=0



                    # if ioVecj:
                    #     print("i", end=" ")
                    # for p in ioVeci:
                    #     print(p, end=" ")
                    # print()
                    # print("j", end=" ")
                    # for p in ioVecj:
                    #     print(p, end=" ")
                    # print()
                        
                    
        for i in range(len(P)):
            if isinstance(P[i],list):
                if P[i][0].ioVec == P[i][1].ioVec:
                    P[i] = 0
        # i = 0
        # while i < len(P):
        #     if P[i]==0:
        #         del P[i]
        #     else:
        #         i+=1
        for p in P:
            if isinstance(p,list):
                for i in p:
                    print(i.ioVec,end=" ")
                print()
            else:
                print(p)
        

        # for i in range(len(P)):
        #     if i == len(P)-1:
        #         path=newRecords[pathsBeginInd[i]:]
        #     else:
        #         path=newRecords[pathsBeginInd[i]:pathsBeginInd[i+1]+1]
        #     print(i)
        #     self.printd("path ", i+1)
        #     for p in P[i]:
        #         self.printd(p)
                
        #     self.printd("end")
            
        

        self.printd("<<==Getting Paths from Record - END ==>>")
        return paths

    

