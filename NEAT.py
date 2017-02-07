# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *

class NEAT:
    def __init__(self, inputNum, outputNum):
        self.inputNum = inputNum
        self.outputNum = outputNum
        self.biasNode = Node(0, tag='Bias Node')
        self.nodeCount = 1

        # input node
        self.inputNodes = []
        for i in range(inputNum):
            self.inputNodes.append(Node(self.nodeCount, tag='Input Node'))
            self.nodeCount += 1

        # hidden node
        self.hiddenNodes = []

        # output node
        self.outputNodes = []
        for j in range(outputNum):
            self.outputNodes.append(Node(self.nodeCount, tag='Output Node'))
            self.nodeCount += 1

        # connection
        self.connections = []
        for i in range(inputNum):
            for j in range(outputNum):
                self.connections.append(Connection(self.inputNodes[i], self.outputNodes[j]))
        for j in range(outputNum):
            self.connections.append(Connection(self.biasNode, self.outputNodes[j]))

        # random weight connection
        for con in self.connections:
            con.randomWeight()



    def showStructure(self):
        print "Total nodes:", self.nodeCount
        print "Connections(%d):"%len(self.connections)
        for con in self.connections:
            print "\t[input]%s %d\t--[%f]--\t[output]%s %d"%(con.input.tag, con.input.id, con.weight, con.output.tag, con.output.id)