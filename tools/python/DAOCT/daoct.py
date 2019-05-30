# -*- coding: utf-8 -*-
"""

@author: Accacio
"""

import utils as ut
import automaton

class DAOCT(ut.MyUtil):
    def __init__(self,files,paramk,verbose,debug):
        ut.MyUtil.__init__(self,verbose,debug)
        self.files = files
        self.k = paramk
        self.tableReader = ut.TableReader(files,verbose,debug)
        self.records = self.tableReader.getRecordFromFile()
        self.paths = self.getPathsFromRecord()
        self.pK, self.sigmaK = self.getModifiedPaths(paramk)
        self.createAutomaton()


    def createAutomaton(self):
        self.printd("<<== Creating Automaton - BEGIN ==>>")
        counter=0
        r=len(self.pK)
        self.X           = []
        self.R           = set()
        self.Sigma       = set()
        self.f           = {}
        self.Lambda      = {}
        self.LambdaTilde = {}
        self.theta       = {}
        self.Gamma       = {}

        # begin of algorithm
        # Line 1
        self.x0 = automaton.State(counter)
        self.LambdaTilde[self.x0] = self.y(self.pK[0][0])
        self.Lambda[self.x0] = self.LambdaTilde[self.x0]

        # Line 2
        self.X.append(self.x0)
        self.printd(self.x0," added to X")
        self.Xf = set()
        # Lines 3 to 19
        for i in range(r):
            self.R.add(i+1)
            l = len(self.pK[i])
            for j in range(l-1):
                self.printd("i=",i,", j=",j)
                # Line 5
                for x_it in self.X:
                    if self.LambdaTilde[x_it] == self.y(self.pK[i][j]):
                        x = x_it
                        self.printd(x," is the state such that $\~{\lambda}(x)=y_{i,j}$")
                        break

                # Lines 6 to 12
                # if self.LambdaTilde[x] != self.y(self.pK[i][j]):
                xPrime = []
                for x_it in self.X:
                    if self.LambdaTilde[x_it] == self.y(self.pK[i][j+1]):
                        xPrime = x_it
                        self.printd(xPrime," is the state such that $\~{\lambda}(x^\prime)=y_{i,j+1}$")
                        break
                if xPrime == []:
                    counter+=1
                    xPrime = automaton.State(counter)
                    self.LambdaTilde[xPrime] = self.y(self.pK[i][j+1])
                    self.Lambda[xPrime] = self.yL(self.pK[i][j+1])
                    self.X.append(xPrime)
                    self.printd(xPrime," added to X")

                self.Sigma.add(self.sigmaK[i][j])
                self.printd(self.sigmaK[i][j])
                sig=self.sigmaK[i][j]
                self.f[(x,sig)] = xPrime
                if xPrime not in self.Gamma:
                    self.Gamma[xPrime] = []
                # print(x , xPrime)
                if x in self.Gamma:
                    if sig not in self.Gamma[x]:
                        self.Gamma[x] += [sig]
                else:
                    self.Gamma[x] = [sig]
                # print("x ",x,self.Gamma[x])
                # print("xPrime ",xPrime,self.Gamma[xPrime])
                self.printd("f(",x,",",sig,") = ", xPrime)
                # Line 14
                if (x,xPrime) in self.theta:
                    if i+1 not in self.theta[(x,xPrime)]:
                        self.theta[(x,xPrime)].add(i+1)
                else:
                    self.theta[(x,xPrime)] = {i+1}
                # Lines 15 to 17
                if j == l - 2:
                    self.Xf.add(xPrime)

        self.printd("<<== Creating Automaton - END ==>>")
        return

    def y(self,vectorm):
        if isinstance(vectorm,list):
            label = ''
            for rec in vectorm:
                label = label + rec.ioVec + ''
        else:
            label = vectorm.ioVec
        return label

    def yL(self,vectorm):
        if isinstance(vectorm,list):
            return vectorm[-1].ioVec
        else:
            return vectorm.ioVec

    def printAutomaton(self):
        # for (x,sig),xprime in self.f.items():
        #     print("f(",x,",",sig,") = ",self.f[(x,sig)],sep="")
        for (x,sig),xout in self.f.items():
            a = map(str,self.theta[(x,xout)])
            theta = ", ".join(a)
            print('f(',x,',',sig,") = ",xout," {",theta,"} \\\\",sep='')
        return




# TODO change to modified paths
    def getAutoTracesFromPath(self,n):
        Q = []
        nodes = n + 1
        pathsList = list(map(lambda path: list(map(lambda node: node.ioVec,path)),self.paths))
        for path in pathsList:
            if len(path) >= nodes:
                # print("path",path)
                # print("path nodes nodes",path[:nodes])
                pathAlreadyAdded=False
                for q in Q:
                    if q == path[:nodes]:
                        pathAlreadyAdded=True
                if not pathAlreadyAdded:
                    Q.append(path[:nodes])
                    # print(Q[-1])
        return len(Q)

    def getAutoTracesFromPathLessN(self,n):
        def getAutoTracesFromPathLessNaux(n,acc):
            if n == 0:
                return 0
            else:
                Q = []
                nodes = n + 1
                pathsList = list(map(lambda path: list(map(lambda node: node.ioVec,path)),self.paths))
                for path in pathsList:
                    if len(path) >= nodes:
                        # print("path",path)
                        # print("path nodes nodes",path[:nodes])
                        pathAlreadyAdded=False
                        for q in Q:
                            if q == path[:nodes]:
                                pathAlreadyAdded=True
                        if not pathAlreadyAdded:
                            Q.append(path[:nodes])
                            # print(Q[-1])

                return len(Q) + getAutoTracesFromPathLessNaux(n-1,acc)
        tracespath =  getAutoTracesFromPathLessNaux(n,0)
        # print ("tracespath",tracespath)
        return tracespath

    def getAutoTracesDAOCT(self,xnode,n,paths):
        if n == 0:
            return 1
        else:
            n = n -1
            result = 0
            for sig in self.Gamma[xnode]:
                paths = set(paths)
                intersPaths = paths.intersection(self.theta[(xnode,self.f[xnode,sig])])
                if sig != []:
                    if intersPaths != set():
                        result = result + self.getAutoTracesDAOCT(self.f[xnode,sig],n,intersPaths)
            return result

    def getAutoTracesDAOCTLessN(self,n):
        def getAutoTracesDAOCTLessNaux(xnode,n,paths,acc):
            if n == 0:
                return 1
            else:
                n = n -1
                for sig in self.Gamma[xnode]:
                    paths = set(paths)
                    intersPaths = paths.intersection(self.theta[(xnode,self.f[xnode,sig])])
                    if sig != []:
                        if intersPaths != set():
                            acc = acc + getAutoTracesDAOCTLessNaux(self.f[xnode,sig],n,intersPaths,0)
                return acc + 1
        tracesDAOCT = getAutoTracesDAOCTLessNaux(self.x0,n,self.R,0) - 1
        # print("traces DAOCT =",tracesDAOCT)
        return tracesDAOCT

    def getExceedingLanguageDAOCTLessN(self,n):
        return self.getAutoTracesDAOCTLessN(n) - self.getAutoTracesFromPathLessN(n)

    def getAutoTracesNDAAO(self,xnode,n):
        if n == 0:
            return 1
        else:
            n = n -1
            result = 0
            for sig in self.Gamma[xnode]:
                if sig != []:
                    result = result + self.getAutoTracesNDAAO(self.f[xnode,sig],n)
            return result

    def getAutoTracesNDAAOLessN(self,n):
        def getAutoTracesNDAAOLessNaux(xnode,n,acc):
            if n == 0:
                return 1
            else:
                n = n -1
                result = 0
                for sig in self.Gamma[xnode]:
                    if sig != []:
                        result = result + getAutoTracesNDAAOLessNaux(self.f[xnode,sig],n,0)
                return result + 1
        return getAutoTracesNDAAOLessNaux(self.x0,n,0) - 1

    def getExceedingLanguageNDAAOLessN(self,n):
        return self.getAutoTracesNDAAOLessN(n) - self.getAutoTracesFromPathLessN(n)

    def graphvizAutomaton(self):
        print('digraph a {')
        print('rankdir=LR;')
        print('# splines = ortho')
        print('ratio=fill')
        print('graph [pad="0.01", nodesep="0.1", ranksep="0.01"];')
        print('node [shape=circle];')
        print('margin=0;')
        print('{rank =same;}')
        print('# size="11.7,8.3!";')
        print('init [style=invis]')
        print('init ->',self.x0)
        for xf in self.Xf:
            print(xf,"[shape=doublecircle];")
        print('')
        for xe,xout in self.f.items():
            a = map(str,self.theta[(xe[0],xout)])
            theta = ",".join(a)
            print((xe[0]),' -> ',xout,' [texlbl="\\scriptsize ',xe[1],",\{",theta,"\}",'"]',sep='')
        print('')
        print('}')
        return

    def printPathd(self,paths):
        if self.debug==True:
            for path in paths:
                print("Path",paths.index(path))
                if isinstance(path,list):
                    for i in path:
                        print(i.ioVec,"",end="")
                else:
                    print(path)
                print()

    def printPath(self,paths):
        for path in paths:
            print("Path",paths.index(path))
            if isinstance(path,list):
                for i in path:
                    print(i.ioVec,"",end="")
            else:
                print(path)
            print()


    def printModifiedPathsd(self,paths):
        if self.debug==True:
            for path in paths:
                print("Path",paths.index(path),":")
                if isinstance(path,list):
                    for i in path:
                        for j in i:
                            print(j.ioVec,"")
                        print()
                else:
                    print(path)
                print()


    def printModifiedPaths(self,paths):
        for path in paths:
            print("Path",paths.index(path),":")
            if isinstance(path,list):
                for i in path:
                    for j in i:
                        print(j.ioVec,"")
                    print()
            else:
                print(path)
            print()


    def getModifiedPaths(self,k):
        self.printd("<<== Getting Modified Paths from Paths - BEGIN ==>>")

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

        sigmaK=[]
        pK=[]
        for path in self.paths:
            newpath = []
            newSigmas = []
            l = len(path)
            self.printd("Path ",self.paths.index(path),":")
            for j in range(l):

                if j<=l-1:
                    if k<=j+1:
                        newVector = path[j-k+1:j+1]

                    elif j+1<k:
                        newVector = path[:j+1]

                    if j<l-1:
                        newSigmas.append(self.getSigma(path[j],path[j+1]))

                    newpath.append(newVector)

                # for i in newVector:
                #     self.printd(i.ioVec)
                # self.printd()


            pK.append(newpath)
            sigmaK.append(newSigmas)

        self.printd("Modified Paths: ")
        self.printModifiedPathsd(pK)

        self.printd("Sigmas: ")
        for sigmas in sigmaK:
            self.printd("Sigma ", sigmaK.index(sigmas),":")
            self.printd()
            self.printdnl("| ")
            for sigma in sigmas:
                self.printdnl(sigma," | ")
            self.printd()

        self.printd("<<== Getting Modified Paths from Paths - END ==>>")
        return (pK, sigmaK)


    def getSigma(self,record,recordPrime):
        vec=record.ioVec
        vecPrime=recordPrime.ioVec
        names=record.ioNames
        diff=[i for i in range(len(vec)) if vec[i] != vecPrime[i]]
        sigma=""
        for i in diff:
            if vec[i]=='0' and vecPrime[i]=='1':
                sigma=sigma + "⬆" + names[i]
            if vec[i]=='1' and vecPrime[i]=='0':
                sigma=sigma + "⬇" + names[i]
        # self.printd("Sigma = ",sigma)
        self.printd(record.ioVec," -> ",recordPrime.ioVec," | ",sigma)
        self.printd()
        return sigma




    def getPathsFromRecord(self):
        self.printd("<<== Getting Paths from Record - BEGIN ==>>")
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
            P.append(path)

        self.printd("==== Removing superposed")

        # pathsNoSuper = []
        # # pathsNoSuper=P.copy()
        # for i in P:
        #     for j in P:
        #         if P.index(i)!=P.index(j):

        #             ioVeci = [rec.ioVec for rec in i]
        #             ioVecj = [rec.ioVec for rec in j]

        #             if ioVecj==ioVeci[:len(ioVecj)]:
        #                 # self.printdnl("Path ", P.index(i), " includes path ", P.index(j))
        #                 print('equal')
        #                 # self.printd(" -> removing path ", P.index(j))
        #             else:
        #                 pathsNoSuper.append(j)
        # self.printPathd(pathsNoSuper)

        self.printd("==== Removing superposed Met-0")
        pathsNoSuper = P.copy()
        for i in range(len(pathsNoSuper)):
            for j in range(len(pathsNoSuper)):
                if i!=j and pathsNoSuper[i]!=0 and pathsNoSuper[j]!=0:
                    ioVeci = [rec.ioVec for rec in pathsNoSuper[i]]
                    ioVecj = [rec.ioVec for rec in pathsNoSuper[j]]
                    if ioVecj==ioVeci[:len(ioVecj)]:
                        self.printdnl("Path ", i, " includes path ",j)
                        self.printd(" -> removing path ",j)
                        pathsNoSuper[j]=0

        i = 0
        while i < len(pathsNoSuper):
            if pathsNoSuper[i]==0:
                del pathsNoSuper[i]
            else:
                i+=1
        self.printPathd(pathsNoSuper)

        #Eliminate paths formed by two elements where both are the initial state
        self.printd("==== Removing 2 node circular path")
        # pathsNoTwoElemCircPath=pathsNoSuper.copy()
        # for i in pathsNoTwoElemCircPath:
        #     if i[0].ioVec == i[1].ioVec:
        #         pathsNoTwoElemCircPath.remove(i)

        pathsNoTwoElemCircPath=list(filter(lambda x: x[0].ioVec!=x[1].ioVec if len(x)>1 else True ,pathsNoSuper))

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
        self.printd("<<== Getting Paths from Record - END ==>>")
        return paths
