
import sys
import csv


class Record: 
    def __init__(self,seq,inputVector,outputVector):
        self.seq = seq
        self.iVec = inputVector
        self.oVec = inputVector

    def __str__(self):
        return str(self.seq) + "," + str(self.vector)

        
    def copyRecord(self):
        return Record(self.seq,self.date,self.utctime,self.timestamp,\
                      self.vector)            



class MyUtil:
    def __init__(self,verbose,debug):
        self.debug=debug
        self.verbose=verbose

    def printv(self,*string):
        if self.verbose==True:
            for i in string:
                print(i, end='')
            print("")

    def printd(self,*string):
        if self.debug==True:
            for i in string:
                print(i, end='')
            print("")
            

class TableReader(MyUtil):
    def __init__(self,files,verbose,debug):
        MyUtil.__init__(self,verbose,debug)
        self.files = files

    def getRecordFromFile(self,numInputs,numOutputs):
        self.printd("<<==Reading Table - BEGIN ==>>")
        readers=[]
        for file in self.files:
            readers.append(csv.DictReader(file,delimiter=','))

        data=[]
        records=[]
        # todo test number of collumns
        for reader in readers:
            lineCount=0
            collumnNames=[]
            for row in reader:
                if lineCount==0:
                    for collumn in row:
                        collumnNames.append(collumn)
                    self.printd("Collumn Names: ",collumnNames)
                    
                if row[collumnNames[0]]!="//END":
                    data.append(row)
                    print(row[collumnNames[1]])
                    
                    inputVector=row
                    outputVector=row
                    records.append(Record(row[collumnNames[0]],inputVector,outputVector))

                    self.printd(row)

                lineCount+=1

        for i in records:
            print("Input Vector", i.iVec)
            print("Output Vector", i.oVec)
        self.printd("<<==Reading Table - END ==>>")
        return (data, collumnNames)

    

