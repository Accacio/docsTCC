def tagger(state):
# state written in base 10 or in binary
    
    AcqValues = []
    AcqValues.append("fmag1")
    AcqValues.append("rmag1")
    AcqValues.append("fmag2")
    AcqValues.append("rmag2")
    AcqValues.append("f3")
    AcqValues.append("r3")
    AcqValues.append("f2")
    AcqValues.append("r2")
    AcqValues.append("f1")
    AcqValues.append("r1")
    AcqValues.append("o")
    AcqValues.append("m")
    AcqValues.append("s3")
    AcqValues.append("s2")
    AcqValues.append("s1")
    AcqValues.append("Pus3")
    AcqValues.append("Pus2")
    AcqValues.append("Pus1")
    AcqValues.append("Amag1")
    AcqValues.append("Retmag1")
    AcqValues.append("Amag2")
    AcqValues.append("Retmag2")
    AcqValues.append("C")


    def f(state):
        if isinstance(state,int):
            
            binstate = bin(state)

            s = list(binstate)

            s.reverse()
            io = []
            for k in range(len(s)):
                if s[k] == '1':
                    io.append(AcqValues[k])
            return io

        if isinstance(state,str):

            s = list(state)
            
            s.reverse()
            io = []
            for k in range(len(s)):
                if s[k] == '1':
                    io.append(AcqValues[k])
            return io

    if isinstance(state,list):

        output = []
        for vector in state:
            output.append(f(vector))
        return output

    return f(state)

def printPath(path):
    c = 0
    for rec in path:
        if isinstance(rec,list):
            for r in rec:
                print(str(c)+': ',r.vector + ', time ' + str(r.time) + 'ms')
            print('\n')
        else:
            v = rec.vector
            t = rec.time
            ios = tagger(v)
            print(str(c)+': ',ios,end=' ')
            print(', time '+str(t)+'ms')
        c+=1    
        
def printPathPrime(path):
    c = 0
    for vec in path:
        if isinstance(vec,list):
            for v in vec:
                print(str(c)+': ',v.vector + ', time ' + str(v.intervals))
            print('\n')
        else:
            u = vec.vector
            t = vec.intervals
            ios = tagger(u)
            print(str(c)+': ',ios,end=' ')
            print(', intervals '+str(t))
        c+=1    

    

        
