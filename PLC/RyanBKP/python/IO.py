def IO(state):
# state written in base 10
    
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
    AcqValues.append("presenceDiscrete")
    AcqValues.append("Pus3")
    AcqValues.append("Pus2")
    AcqValues.append("Pus1")
    AcqValues.append("Amag1")
    AcqValues.append("Retmag1")
    AcqValues.append("Amag2")
    AcqValues.append("Retmag2")
    AcqValues.append("C")

    binstate = bin(state)

    s = list(binstate)
    s.reverse()
    io = []
    for k in range(len(s)):
        if s[k] == '1':
            io.append(AcqValues[k])
    return io
