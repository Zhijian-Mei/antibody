def freq(ls, k):
    freqTable = {}

    for i in ls:
        for j in range(len(i)-k+1):
            kmer = i[j:j+k]
            if kmer in freqTable:
                freqTable[kmer][0] += 1
            else:
                freqTable[kmer] = [1]

    for key in freqTable:
        stInt = []
        for i in key:
            stInt.append(ord(i))

        stPrefix = [sum(stInt[:i+1]) for i in range(len(key))]

        freqTable[key].append(stPrefix)

    return freqTable


def errorCorrectionDict(ls, k):
    freqTable = freq(ls, k)
    errorCorrectionDict = {}

    for key in freqTable:
        prefix1 = freqTable[key][1]
        for i in freqTable:
            prefix2 = freqTable[i][1]
            diff = 0
            for j in range(len(prefix1)):
                if prefix1[j] != prefix2[j]:
                    diff += 1
            if diff == 1:
                if prefix1[-1] == prefix2[-1]:
                    errorCorrectionDict[key] = i

    return errorCorrectionDict


# input reads, return corrected reads, this list contains score
# iterate from 8mer to 5mer
def errorCorrection(ls):
    for a in range(4):

        reads = []
        for i in ls:
            if len(i[0]) >= (8-a):
                reads.append(i[0])

        errorDict = errorCorrectionDict(reads, (8-a))

        for i in ls:
            for j in errorDict:
                if j in i[0]:
                    i[0] = i[0].replace(j, errorDict[j])

    return ls
