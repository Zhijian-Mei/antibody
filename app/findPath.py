import csv
import sys
import re
import debruijn


def path(filelist):

    sys.setrecursionlimit(30000)

    csv.register_dialect('mydialect', delimiter='\t', quoting=csv.QUOTE_ALL)

    inputs = []
    # removeList = '1234567890.+-'

    # perform different filtering rules upon different files
    for f in filelist:
        with open(f,) as csvfile:
            file_list = csv.reader(csvfile, 'mydialect')
            next(file_list)
            if f.rsplit('.')[2] == 'mzid':
                for line in file_list:
                    if float(line[-2]) <= 0.01:
                        # read = line[9]
                        read = ''.join(re.split('[1234567890.+-]', line[9]))
                        # read = re.sub('[1234567890.+-]','',line[9])
                        # for i in removeList:
                        #     read = read.replace(i,'')
                        # if read not in inputs:
                        #     inputs.append(read)
                        inputs.append([read, (1-float(line[-2]))])
                        # if len(inputs) > 191:
                        #     print(read)
                        #     break
            else:
                for line in file_list:
                    if line[2] != 'Score':
                        if float(line[2]) >= 0.6:
                            inputs.append([line[1], float(line[2])])

    csv.unregister_dialect('mydialect')

    inputs1 = inputs
    delList = []

    for i in inputs1:
        if 'LLLLLL' in i[0]:
            delList.append(i)
        elif 'PPPPPP' in i[0]:
            delList.append(i)
        elif 'GGGGGG' in i[0]:
            delList.append(i)
        elif 'SSSSSS' in i[0]:
            delList.append(i)
        elif 'KKKKKK' in i[0]:
            delList.append(i)

    for i in delList:
        inputs1.remove(i)

    inputsBefore = []

    for i in inputs1:
        if len(i[0]) > 5:
            inputsBefore.append(i)

    # graphkmer = debruijn.DeBruijnGraph(inputsBefore, 5)
    # pathkmer = graphkmer.longestPath()
    # removeList = []
    # inputsBefore = []

    # for i in inputsBefore:
    #     for j in pathkmer:
    #         if i[0] in j[1][0]:
    #             removeList.append(i)

    # for i in removeList:
    #     inputsBefore.remove(i)

    for a in range(10):

        inputskmer = []

        for i in inputsBefore:
            if len(i[0]) > (5+a):
                inputskmer.append(i)

        graphkmer = debruijn.DeBruijnGraph(inputskmer, 5 + a)
        pathkmer = graphkmer.longestPath()

        removeList = []
        inputsBefore = []

        for i in inputskmer:
            for j in pathkmer:
                if i[0] in j[1][0]:
                    removeList.append(i)

        for i in removeList:
            inputskmer.remove(i)

        for i in inputskmer:
            inputsBefore.append(i)

        for i in pathkmer:
            inputsBefore.append(i[1])

        # print(pathkmer)

    pathkmer1 = []
    lengthList = []
    for i in pathkmer:
        lengthList.append(i[0])

    lengthList.sort()

    for i in lengthList:
        for j in pathkmer:
            if i == j[0]:
                pathkmer1.append([j[0], j[1][0]])

    return pathkmer1
