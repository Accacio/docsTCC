# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 22:00:42 2018

@author: Ryan
"""

from collections import deque

class Vertex:
    def __init__(self,label):
        self.label = str(label)


class Graph:
    def __init__(self,Adj):
        self.Adj = Adj
        self.nbVertices = len(Adj)
        self.V = [v for v in Adj]
        for v in Adj:
            for u in Adj[v]:
                if u not in Adj:
                    self.V.append(u)

    def BFS(self,s):
        for u in self.V:
            if u!=s:
                u.color = 'white'
                u.d = float('inf')
                u.pi = None
        s.color = 'gray'
        s.d = 0
        s.pi = None
        Q = deque([s])
        while len(Q) > 0:
            u = Q.popleft()
            for v in self.Adj[u]:
                if v.color == 'white':
                    v.color = 'gray'
                    v.d = u.d + 1
                    v.pi = u
                    Q.append(v)
            u.color = 'black'

    def DFS(self,topologicalSort=False,vertices='all'):
        for u in self.V:
            u.color = 'white'
            u.pi = None
        self.time = 0
        if vertices == 'all':
            V = self.V
        else:
            V = vertices
        for u in V:
            if u.color == 'white':
                self.DFSvisit(u,topologicalSort)
        self.time = 0

    def DFSvisit(self,u,topologicalSort=False,scc=False,ind=None):
        self.time+=1
        u.d = self.time
        u.color = 'gray'
        for v in self.Adj[u]:
            if v.color == 'white':
                v.pi = u
                self.DFSvisit(v,topologicalSort,scc,ind)
        u.color = 'black'
        self.time+=1
        u.f = self.time
        if topologicalSort:
            self.topSortedList = [u] + self.topSortedList
        if scc:
            self.SCCtrees[ind].append(u)

    def TopologicalSort(self):
        self.topSortedList = list()
        self.DFS(True)
        return self.topSortedList

    def StronglyConnectedComponents(self):
        self.TopologicalSort()
        GT = self.transposeGraph()
        GT.SCCtrees = []
        for u in GT.V:
            u.color = 'white'
            u.pi = None
        GT.time = 0
        ind = 0
        for u in self.topSortedList:
            if u.color == 'white':
                GT.SCCtrees.append([])
                GT.DFSvisit(u,False,True,ind)
                ind+=1
        GT.time = 0
        return GT.SCCtrees

    def maxNumberOfTransitionsBeforeVertex(self):
        self.TopologicalSort()
        w = {}
        for u in self.V:
            for v in self.V:
                w[(u,v)] = 0
        for u in self.Adj:
            for v in self.Adj[u]:
                w[(u,v)] = 1
        #eta = len(self.V)
        l = {}
        for vj in self.topSortedList:
            l[vj] = 0
        for v in self.topSortedList:
            lcandidates = []
            for u in self.Adj:
                lcandidates.append(l[u] + w[(u,v)])
            l[v] = max(lcandidates)
        return l

    def transposeGraph(self):
        AdjT = {}
        for u in self.V:
            AdjT[u] = []
        for u in self.V:
            for v in self.Adj[u]:
                AdjT[v].append(u)
        GT = Graph(AdjT)
        return GT

