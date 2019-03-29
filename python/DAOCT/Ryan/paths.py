#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 22:06:51 2018

@author: Ryan
"""

import table_read
import IO
import daoct

def pathsConstructionFromFiles(*filenames):

    records = table_read.readRecordsFromFiles(*filenames)

    #Exclude the neighbours vectors that are equal
    recordsn = [records[0]]
    for i in range(len(records) - 1):
        if records[i].vector!=records[i+1].vector or records[i].vector==records[0].vector:
            recordsn.append(records[i+1])
        #else: print(i)

    #Find the vectors that are equal to the first one to separate the paths
    ind = [0]
    for i in range(1,len(recordsn)):
        if recordsn[0].vector==recordsn[i].vector:
            ind.append(i)

    #Obtain the candidates to paths
    P = []
    for i in range(len(ind) - 1):
        P.append(recordsn[ind[i]:ind[i+1]+1])
        recordsn[ind[i+1]] = recordsn[ind[i+1]].copyRecord()

    #Change definition of time so as to represent durations of transitions
    #x0.time is the time between recordings of x0 and of the next state
    #The times corresponding to the initial state are set to 'x ' because they are
    #   not relevant to diagnosis
    for p in P:
        for i in range(len(p)-1):
            p[i].time = p[i+1].time - p[i].time
            p[i].minTime = p[i].time
            p[i].maxTime = p[i].time
        p[0].time = 'x '
        p[0].minTime = p[0].time
        p[0].maxTime = p[0].time
        p[-1].time = 'x '
        p[-1].minTime = p[-1].time
        p[-1].maxTime = p[-1].time

    #Eliminate the paths that are contained in a longer path keeping the longest
    #    time durations
    #similarPaths = []
    #visitedPaths = []
    for i in range(len(P)):
        for j in range(len(P)):
            if i!=j and P[i]!=0 and P[j]!=0:
                if len(P[i])<=len(P[j]):
                    veci = [rec.vector for rec in P[i]]
                    vecj = [rec.vector for rec in P[j]]
                    if veci==vecj[:len(veci)]:
                        for q in range(len(veci)):
                            P[j][q].time = max([P[j][q].time,P[i][q].time])
                            P[j][q].minTime = min([P[j][q].minTime,P[i][q].minTime])
                            P[j][q].maxTime = max([P[j][q].maxTime,P[i][q].maxTime])
                        P[i] = 0


    #Eliminate paths formed by two elements where both are the initial state
    for i in range(len(P)):
        if isinstance(P[i],list):
            if P[i][0].vector == P[i][1].vector:
                P[i] = 0

    #Remove grey paths
    #P = removeGreyPaths(P)

    #Path elimination
    i = 0
    while i < len(P):
        if P[i]==0:
            del P[i]
        else:
            i+=1
    return P

#def removeGreyPaths(P):
#    for i in range(len(P)):
#        if isinstance(P[i],list):
#            if P[i][1].vector == '00001000000001010101010':
#                P[i] = 0
#    i = 0
#    while i < len(P):
#        if P[i]==0:
#            del P[i]
#        else:
#            i+=1
#    return P

def pathDistinction(P,i):
    path = [rec.vector for rec in P[i]]
    diffindex = []
    for j in range(len(P)):
        if i!=j:
            p = [rec.vector for rec in P[j]]
            for q in range(min([len(path),len(p)])):
                if path[q]!=p[q]:
                    break
            diffindex.append(q)
    return max(diffindex)

def nbOfCycles(*filenames):
    records = table_read.readRecordsFromFiles(*filenames)
    c = -1
    for rec in records:
        if rec.vector == records[0].vector: c+=1
    return c

P = pathsConstructionFromFiles('DATA_IDENTIFICATION_BESTSOFAR.csv',
                               'DATA_IDENTIFICATION_BESTSOFAR2.csv')
G = daoct.DAOCT(P,1)
G.printAutomaton()
