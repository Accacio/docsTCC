# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 17:56:04 2018

@author: Ryan
"""
import automaton
import table_read
import IO

class DAOCT(automaton.DeterministicAutomaton):
    
    def __init__(self,P,k):
        self.Pk = []
        for p in P:
            self.Pk.append(self.newPath(p,k))    
        self.__construction(self.Pk)
        
    def __construction(self,Pk):
        counter = 0
        self.Lambda = {}
        self.LambdaTilde = {}
        self.x0 = automaton.State(counter)
        self.X = []
        self.X.append(self.x0)
        self.Lambda[self.X[0]] = self.y(Pk[0][0])
        self.LambdaTilde[self.X[0]] = self.Lambda[self.X[0]]
        self.theta = {}
        self.f = {}
        self.Sigma = set()
        self.Events = {}
        self.Xf = set()
        r = len(Pk)
        for i in range(r):
            li = len(Pk[i])
            for j in range(li - 1):
                for x in self.X:
                    if self.LambdaTilde[x] == self.y(Pk[i][j]):
                        curr = x
                        break
                foundxprime = 0
                for x in self.X:
                    if self.LambdaTilde[x]==self.y(Pk[i][j+1]):
                        foundxprime = 1
                        xprime = x
                        break
                if not foundxprime:
                    counter+=1
                    xprime = automaton.State(counter)
                    self.X.append(xprime)
                    self.LambdaTilde[xprime] = self.y(Pk[i][j+1])
                    self.Lambda[xprime] = self.yL(Pk[i][j+1])
                sigma = self.getEvent(self.Lambda[curr],self.Lambda[xprime])
                self.Sigma.add(sigma)
                self.f[(curr,sigma)] = xprime
                if (curr,xprime) in self.theta:
                    self.theta[(curr,xprime)].append(i)
                else:
                    self.theta[(curr,xprime)] = [i]
                if j == li - 2: self.Xf.add(xprime)
                    
    def y(self,vectorm):
        if isinstance(vectorm,list):
            label = ''
            for rec in vectorm:
                label = label + rec.vector + ''
        else:
            label = vectorm.vector
        return label
    
    def yL(self,vectorm):
        if isinstance(vectorm,list):
            return vectorm[-1].vector
        else:
            return vectorm.vector
    
    def newPath(self,path,k):
        if k>1:
            newpath = []
            l = len(path)
            for j in range(l):
                if k<=j+1 and j<=l-1:
                    newvector = path[j-k+1:j+1]
                if j+1<k:
                    newvector = path[:j+1]
                newpath.append(newvector)
        else:
            newpath = path
        return newpath
    
    def getReachableStates(self,curr):
        #curr = self.getStateFromVector(currVector)
        #reachVectors = []
        reachStates = set()
        for state in self.X:
            if (curr,state) in self.theta:
                reachStates.add(state)
        return reachStates
    
    def getStatesFromVector(self,vector):
        possStates = set()
        for x in self.X:
            if self.Lambda[x] == vector: possStates.add(x)
        return possStates
            
    def getEvent(self,vecin,vecout):
        N = table_read.ioVectorLength
        event = ''
        for i in range(len(vecin)):
            if vecin[i]!=vecout[i]:
                kvector = '0'*i+'1'+'0'*(N-i-1)
                e = IO.tagger(kvector)[0]
                #e = str(i)
                if vecin[i]=='0': 
                    event = event + e + '_1 '
                else: event = event + e + '_0 '
        if event=='': return 'Equal vectors!'
        return event                     
    
    def printAutomaton(self):
        print('States: ',end='')
        for x in self.X:
            print(x.label,end=' ')
#        print('\nEvents: ',end='')
#        for sigma in self.Sigma:
#            print(sigma.label,end=' ')
        print('\nTransition function (xin,event) --> xout')
        for xe,xout in self.f.items():
            print((int(xe[0].label),xe[1]),' --> ',xout.label)
            print('\n')
        print('\nInitial state: '+str(self.x0.label))
        print('\n\nTheta (xin,xout) --> set of paths from xin to xout')
        for x,paths in self.theta.items():
            print((int(x[0].label),int(x[1].label)),' --> ',paths)
##        for x,paths in self.theta.items():
##            print((x[0].label,x[1].label),' --> ',paths,' MaxTime:',\
##                  str(max(self.thetaTimes[x]))+'ms')    
        print('\n-----------')  

#G = DAOCT(P,2)