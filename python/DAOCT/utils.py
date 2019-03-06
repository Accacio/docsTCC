
import sys
import csv


class Record: 
    def __init__(self,seq,date,utctime,time,iovector):
        self.seq = seq
        self.date = date
        self.utctime = utctime
        self.timestamp = time
        self.vector = iovector
        self.__timeConversion()
        self.minTime = self.time
        self.maxTime = self.time
        #self.times = []
        
    def __timeConversion(self):
        t = self.timestamp
        tsplit = t.split(':')
        secsplit = tsplit[-1].split('.')
        timeInMilisseconds = 60*60*1000*int(tsplit[0]) + \
        60*1000*int(tsplit[1]) + 1000*int(secsplit[0]) + int(secsplit[1])
        self.time = timeInMilisseconds    
        
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
    def __init__(self,file,verbose,debug):
        MyUtil.__init__(self,verbose,debug)
        self.file = file


        

    def readTable(self):
        reader = csv.DictReader(self.file,delimiter=',')
        collumNames=[]
        data=[]
        # print(reader.rows)
        lineCount=0
        for row in reader:
            if lineCount==0:
                for collum in row:
                    collumNames.append(collum)
            data.append(row)
            self.printd(row)
            lineCount+=1
        return (data, collumNames)

    

