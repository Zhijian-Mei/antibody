
import networkx as nx
import matplotlib.pyplot as plt
import errorCorrection


class DeBruijnGraph:
    # a de bruijn multigraph built from a collection of strings

    # split the input string into (k+1)-mer substrings
    @staticmethod
    def chop(st, k):

        # raise error if inputs are unusual
        if len(st) - k < 0:
            raise Exception(st + " Some of the reads are smaller than k.")

        for i in range(len(st)-k):
            yield st[i:i+k+1]

    class Node:
        # node in a de bruijn graph, representing a k-mer

        def __init__(self, kmer, score):
            self.kmer = kmer
            self.score = score

        def changeScore(self, newScore):
            self.score = newScore

        def __hash__(self):
            return hash(self.kmer)

    def __init__(self, strIter, k):

        self.G = {}  # multimap from nodes to neighbours
        self.nodes = {}  # maps k-mers to Node objects
        self.k = k
        strIter = errorCorrection.errorCorrection(strIter)

        for st in strIter:
            # if len(st) == k:
            #     if st not in self.nodes:
            #         self.nodes[st] = self.Node(st)
            for kp1mer in self.chop(st[0], k):
                kmerL, kmerR = kp1mer[:-1], kp1mer[1:]
                nodeL, nodeR = None, None
                if kmerL in self.nodes:
                    if st[1] > self.nodes[kmerL].score:
                        self.nodes[kmerL].changeScore(st[1])
                    nodeL = self.nodes[kmerL]
                else:
                    # if nodeL == None:
                    nodeL = self.nodes[kmerL] = self.Node(kmerL, st[1])
                if kmerR in self.nodes:
                    if st[1] > self.nodes[kmerR].score:
                        self.nodes[kmerR].changeScore(st[1])
                    nodeR = self.nodes[kmerR]
                else:
                    # if nodeR == None:
                    nodeR = self.nodes[kmerR] = self.Node(kmerR, st[1])
                self.G.setdefault(nodeL, [])
                if nodeR not in self.G[nodeL]:
                    if nodeL.kmer != nodeR.kmer:
                        self.G[nodeL].append(nodeR)

        for i in range(len(strIter)-1):
            for j in strIter[i+1:len(strIter)]:
                if strIter[i][0][:k-1] == j[0][-k+1:]:
                    kmerR = strIter[i][0][:k]
                    kmerL = j[0][-k:]

                    nodeR = self.nodes[kmerR]
                    nodeL = self.nodes[kmerL]
                    self.G.setdefault(nodeL, [])
                    if nodeR not in self.G[nodeL]:
                        if nodeL.kmer != nodeR.kmer:
                            self.G[nodeL].append(nodeR)

                if strIter[i][0][-k+1:] == j[0][:k-1]:
                    kmerR = j[0][:k]
                    kmerL = strIter[i][0][-k:]

                    nodeR = self.nodes[kmerR]
                    nodeL = self.nodes[kmerL]
                    self.G.setdefault(nodeL, [])
                    if nodeR not in self.G[nodeL]:
                        if nodeR.kmer != nodeL.kmer:
                            self.G[nodeL].append(nodeR)

    def errorTolerance(self, nodeA, nodeB):
        # same letters and one swap

        nodeAdic = {}
        nodeBdic = {}
        swap = 0

        for i in range(len(nodeA)):
            if nodeA[i] in nodeAdic:
                nodeAdic[nodeA[i]][0] += 1
                nodeAdic[nodeA[i]].append(i)
            else:
                nodeAdic[nodeA[i]] = [1, i]

        for i in range(len(nodeB)):
            if nodeB[i] in nodeBdic:
                nodeBdic[nodeB[i]][0] += 1
                nodeBdic[nodeB[i]].append(i)
            else:
                nodeBdic[nodeB[i]] = [1, i]

        # check that nodeA and nodeB contain the same letters
        # and each of them has the same occurrence
        for key, value in nodeAdic.items():
            if key not in nodeBdic:
                return False
            elif value[0] != nodeBdic[key][0]:
                return False

        for i in nodeAdic:
            del nodeAdic[i][0]

        for i in nodeBdic:
            del nodeBdic[i][0]

        # check that there is only one swap existed
        for key, value in nodeAdic.items():
            indexKey = nodeBdic[key]
            for i in indexKey:
                swapLetter = nodeA[i]
                if swapLetter != key:
                    indexSwap = nodeBdic[swapLetter]
                    for j in value:
                        if j in indexSwap:
                            swap += 1

        if swap == 2:
            return True

        return False

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph

    def visualize(self):
        graph = nx.DiGraph()
        for i in self.G:
            for j in self.G[i]:
                graph.add_edge(i.kmer, j.kmer)
        nx.draw_networkx(graph)
        plt.show()

    def isCyclicUtil(self, v, visited, recStack):

        # mark current node as visited
        # add to recursion stack
        visited[v] = True
        recStack[v] = True

        nodesList = list(self.nodes.keys())

        # recur for all neighbors
        # if any neighbor is visited and in recStack then graph is cyclic
        if self.nodes[nodesList[v]] in self.G:
            # this gives a list of nodes
            for neighbor in self.G[self.nodes[nodesList[v]]]:
                u = nodesList.index(neighbor.kmer)
                if visited[u] == False:
                    if self.isCyclicUtil(u, visited, recStack) == True:
                        return True
                elif recStack[u] == True:
                    return True

        # the node needs to be poped from recursion stack before function ends
        recStack[v] = False
        return False

    # returns true if graph is cyclic else false
    def isCyclic(self):

        v = len(self.nodes)

        visited = [False] * v
        recStack = [False] * v

        for node in range(v):

            if visited[node] == False:

                if self.isCyclicUtil(node, visited, recStack) == True:

                    # print out nodes in the loop
                    # curNode = list(self.nodes.keys())[node]
                    # print(curNode)
                    # thisNode = self.nodes[curNode]
                    # nextNodeList = self.G[thisNode]
                    # if len(nextNodeList) == 1:
                    #     nextNode = nextNodeList[0]
                    #     while nextNode != thisNode:
                    #         print(nextNode.kmer)
                    #         nextNodeList = self.G[nextNode]
                    #         if len(nextNodeList) > 1:
                    #             break
                    #         nextNode = nextNodeList[0]
                    #         nextNodeList = self.G[thisNode]

                    return True

        return False

    def topoSortVisit(self, s, visited, sortlist):
        visited[s] = True

        rev = self.revG()

        if s in rev:  # not head node
            for i in rev[s]:
                if not visited[i]:
                    self.topoSortVisit(i, visited, sortlist)
        sortlist.append(s)

    def topoSort(self):
        visited = {i: False for i in self.nodes.values()}

        sortlist = []

        for v in self.nodes.values():
            if not visited[v]:
                self.topoSortVisit(v, visited, sortlist)

        return sortlist

    # compute G with each edge reversed

    def revG(self):

        revGraph = {}

        for a, b in self.G.items():
            for i in range(len(b)):
                if b[i] in revGraph.keys():
                    revGraph[b[i]].append(a)
                else:
                    revGraph[b[i]] = [a]
        return revGraph

    # remove kmers already seen in the longest path
    def removeNodes(self, path):

        k = self.k

        for i in range(len(path)-k):

            kmerStr = path[i:i+k]
            print(kmerStr)
            if kmerStr in self.nodes:
                kmer = self.nodes[kmerStr]
                del self.G[kmer]
                for key, value in self.G.items():
                    if kmer in value:
                        self.G[key].remove(kmer)
                del self.nodes[kmerStr]

    # remove circle nodes in graph
    def removeCircle(self):

        delNode = []

        for a, b in self.G.items():
            if len(b) > 1:
                delNode.append(a)

        for i in delNode:
            del self.G[i]

        for a, b in self.G.items():
            for i in b:
                if i in delNode:
                    self.G[a].remove(i)

    # longest path in the graph

    def longestPath(self):

        self.removeCircle()

        k = self.k

        if self.isCyclic() == 1:
            # self.visualize()
            raise Exception(
                "The De Bruijn graph is cyclic and would not be able to identify the longest path.")

        pathsDic = {}

        rev = self.revG()
        for v in self.topoSort():
            if v not in rev:
                pathsDic[v] = [self.k, [v.kmer, v.score]]
            else:
                preNode = rev[v]
                distList = []
                preMaxNodeIndex = []
                preMaxNode = []
                for i in preNode:
                    preNodePath = pathsDic[i]
                    distList.append(preNodePath[0])
                maxDist = max(distList)
                for i in range(distList.count(maxDist)):
                    maxIndex = distList.index(maxDist)
                    preMaxNodeIndex.append(maxIndex)
                    distList[maxIndex] = -1
                for i in preMaxNodeIndex:
                    preMaxNode.append(preNode[i])
                maxNode = []
                for i in preMaxNode:
                    preMaxPath = pathsDic[i][1:]
                    for j in preMaxPath:
                        maxNode.append([j[0]+v.kmer[-1], j[1]*v.score])
                pathsDic[v] = [maxDist+1]
                pathsDic[v].extend(maxNode)

        distLists = pathsDic.values()
        distList = []
        for i in distLists:
            distList.append(i[0])
        if len(distList) != 0:
            maxDist = max(distList)
        nodeList = []
        for key, value in pathsDic.items():
            # if value[0] == maxDist:
            if value[0] >= (3*k-1):
                nodeList.append(key)
        result = []
        for i in nodeList:
            eq = False
            for j in result:
                if pathsDic[i][0] <= j[0]:
                    if j[1][0][:pathsDic[i][0]] == pathsDic[i][1][0]:
                        eq = True
                else:
                    if pathsDic[i][1][0][:j[0]] == j[1][0]:
                        result.remove(j)
            if eq == False:
                for a in range(len(pathsDic[i])-1):
                    result.append([pathsDic[i][0], pathsDic[i][a+1]])

        delList = []
        for a in range(len(result)-1):
            for b in result[a+1:len(result)]:
                if result[a][0] == b[0]:
                    diff = 0
                    for c in range(result[a][0]):
                        if result[a][1][0][c] != b[1][0][c]:
                            diff += 1
                    if diff == 1:
                        if result[a][1][1] > b[1][1]:
                            if b not in delList:
                                delList.append(b)
                        else:
                            if result[a] not in delList:
                                delList.append(result[a])
        for i in delList:
            result.remove(i)

        # result1 = []
        # for i in result:
        #     result1.append([i[0], i[1][0]])

        return result
