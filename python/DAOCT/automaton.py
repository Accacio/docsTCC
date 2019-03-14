# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:37:37 2018

@author: Ryan
"""

import graph

class State(graph.Vertex):
    def __init__(self,labels):
        #self.labels = labels
        if isinstance(labels,(int,str)):
            self.labels = labels
            self.label = str(labels)
            return
        if isinstance(labels,(set)):
            self.states = labels
            labels = [x.label for x in labels]
            labels = tuple(labels)
        self.label = []
        self.improveLabel(labels)
        self.labels = tuple(self.label)
        #self.label = str(self.labels)
        self.label = self.labels

    def improveLabel(self,l):
        for p in l:
            if isinstance(p,tuple)==False:
                self.label.append(p)
            else:
                #print('Improve label loop!')
                self.improveLabel(p)

    def __str__(self):
        return "x" + self.label

class Event:
    def __init__(self,label):
        self.label = str(label)

class DeterministicAutomaton(graph.Graph):
    def __init__(self,X,Sigma,f,x0,Xm=set()):
        self.X = X
        self.Sigma = Sigma
        self.f = f
        self.x0 = x0
        self.Xm = Xm
        self.V = self.X
        self.unobservable = set()
        self.unobervableSets = []
        self.observableSets = []
        self.faults = set()
        for xe in self.f:
            if xe[0] not in X:
                self.X.add(xe[0])
            if xe[1] not in Sigma:
                self.Sigma.add(xe[1])
        if x0 not in self.X:
            self.X.add(x0)
        for x in self.Xm:
            if x not in self.X:
                self.X.add(x)
        self.Adj = {}
        for x in self.X:
            self.Adj[x] = []
        for xe in self.f:
            self.Adj[xe[0]].append(self.f[xe])

    def gamma(self,x):
        activeEvents = set()
        for sigma in self.Sigma:
            if (x,sigma) in self.f:
                activeEvents.add(sigma)
        return activeEvents

    def ac(self):
        Xac = set()
        fac = {}
        Xmac = set()
        self.BFS(self.x0)
        for x in self.X:
            if x.d != float('inf'):
                Xac.add(x)
        for xe in self.f:
            if (xe[0] in Xac)&(self.f[xe] in Xac):
                fac[xe] = self.f[xe]
        Xmac = self.Xm.intersection(Xac)
        return DeterministicAutomaton(Xac,self.Sigma,fac,self.x0,Xmac)

    def coac(self):
        Xcoac = set()
        fcoac = {}
        T = self.transposeGraph()
        #for x in self.Xm:
        #    T.BFS(x)
        T.DFS(vertices=self.Xm)
        for x in self.X:
            if x.color != 'white':
                Xcoac.add(x)
        for xe in self.f:
            if (xe[0] in Xcoac)&(self.f[xe] in Xcoac):
                fcoac[xe] = self.f[xe]
        if self.x0 in Xcoac:
            x0coac = self.x0
        else:
            x0coac = None
        return DeterministicAutomaton(Xcoac,self.Sigma,fcoac,x0coac,self.Xm)

    def trim(self):
        return self.ac().coac()

    def product(self,arg):
        xprod = set()
        xmprod = set()
        fprod = {}
        stateDict = {}
        for x1 in self.X:
            for x2 in arg.X:
                newState = State((x1.labels,x2.labels))
                xprod.add(newState)
                stateDict[(x1.label,x2.label)] = newState
                if x1 in self.Xm and x2 in arg.Xm:
                    xmprod.add(newState)
                if x1 is self.x0 and x2 is arg.x0:
                    x0prod = newState
        for x1 in self.X:
            for x2 in arg.X:
                for sigma in self.gamma(x1).intersection(arg.gamma(x2)):
                    f1 = self.f[(x1,sigma)].label
                    f2 = arg.f[(x2,sigma)].label
                    fprod[(stateDict[x1.label,x2.label],sigma)] = \
                    stateDict[(f1,f2)]
        events = self.Sigma.union(arg.Sigma)
        return DeterministicAutomaton(xprod,events,fprod,x0prod,xmprod).ac()

    def parallel(self,arg):
        xpar = set()
        xmpar = set()
        fpar = {}
        stateDict = {}
        for x1 in self.X:
            for x2 in arg.X:
                newState = State((x1.labels,x2.labels))
                newState.states = (x1,x2)
                xpar.add(newState)
                stateDict[(x1.label,x2.label)] = newState
                if x1 in self.Xm and x2 in arg.Xm:
                    xmpar.add(newState)
                if x1 is self.x0 and x2 is arg.x0:
                    x0par = newState
        for x1 in self.X:
            for x2 in arg.X:
                for sigma in self.gamma(x1).intersection(arg.gamma(x2)):
                    f1 = self.f[(x1,sigma)].label
                    f2 = arg.f[(x2,sigma)].label
                    fpar[(stateDict[x1.label,x2.label],sigma)] = \
                    stateDict[(f1,f2)]
                for sigma in self.gamma(x1).difference(arg.Sigma):
                    f1 = self.f[(x1,sigma)].label
                    fpar[(stateDict[x1.label,x2.label],sigma)] = \
                    stateDict[(f1,x2.label)]
                for sigma in arg.gamma(x2).difference(self.Sigma):
                    f2 = arg.f[(x2,sigma)].label
                    fpar[(stateDict[x1.label,x2.label],sigma)] = \
                    stateDict[(x1.label,f2)]
        events = self.Sigma.union(arg.Sigma)
        par = DeterministicAutomaton(xpar,events,fpar,x0par,xmpar).ac()
        par.addUnobservableEvents(self.unobservable.union(arg.unobservable))
        par.addFaultEvents(self.faults.union(arg.faults))
        return par

    def addUnobservableEvents(self,uo):
        for sigma in uo:
            self.unobservable.add(sigma)

    def addFaultEvents(self,f):
        for sigma in f:
            self.faults.add(sigma)

    def uR(self,B):
        ur = set()
        adj = {}
        for x in self.X:
            adj[x] = []
        for xe in self.f:
            if xe[1] in self.unobservable:
                adj[xe[0]].append(self.f[xe])
        G = graph.Graph(adj)
        for x in B:
            G.BFS(x)
            for u in G.V:
                if u.d != float('inf'):
                    ur.add(u)
        return ur

    def addSubsetOfObservableEvents(self,obs):
        self.observableSets.append(obs)
        unobs = self.Sigma.difference(obs)
        self.unobervableSets.append(unobs)

    def printAutomaton(self):
        print('States: ',end='')
        for x in self.X:
            print(x.label,end=' ')
        print('\nEvents: ',end='')
        for sigma in self.Sigma:
            print(sigma.label,end=' ')
        print('\nTransition function (xin,event) --> xout')
        for xe,xout in self.f.items():
            print((xe[0].label,xe[1].label),' --> ',xout.label)
        print('Initial state: '+str(self.x0.label))
        print('Marked states: ',end='')
        for x in self.Xm:
            print(x.label,end=' ')
        if len(self.unobservable) > 0:
            print('\nUnobservable events: ',end='')
            for sigma in self.unobservable:
                print(sigma.label,end=' ')
        if len(self.faults) > 0:
            print('\nFault events: ',end='')
            for sigma in self.faults:
                print(sigma.label,end=' ')
        print('\n-----------')



