# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *
import math

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
            print "\t[%s %d] = %f\t--[%f]--\t[%s %d] = %f"%(con.input.tag, con.input.id, con.input.value,
                                                             con.weight,
                                                             con.output.tag, con.output.id, con.output.value)

    def sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-z))

    def tanh(self, z):
        return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

    def updateNode(self, id):
        sum = 0
        for con in self.connections:
            if con.output.id == id:
                sum += con.input.value * con.weight
        return self.sigmoid(sum)

    def forwardPropagation(self):
        for hid in self.hiddenNodes:
            hid.value = self.updateNode(hid.id)

        for out in self.outputNodes:
            out.value = self.updateNode(out.id)
