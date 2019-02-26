# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 18:38:08 2018

@author: Ryan
"""

import csv

ioVectorLength = 23

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

def readRecordsFromFiles(*filenames):
    readers = []
    for filename in filenames:
        file = open(filename,newline='')
        readers.append(csv.DictReader(file,delimiter=','))
    
    records = []
    for reader in readers:
        for row in reader:
            if row['SeqNo'] != '//END':
                records.append(Record(int(row['SeqNo']),row['Date'],row['UTC Time'],\
                                  row['Time'],int(row['IOvector'])))    
        
    for rec in records:
        vec = bin(rec.vector)[2:]
        #vec = [int(b) for b in vec]
        rec.vector = '0'*(ioVectorLength - len(vec)) + vec 
        
        
        
    return records
