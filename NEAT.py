# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *
# from Environment import Environment

import math

class NEAT:
    connectionList = []
    @staticmethod
    def sigmoid(z):
        return 1.0 / (1.0 + math.exp(-z))

    @staticmethod
    def tanh(z):
        return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

    @staticmethod
    def probability(p):
        "The probability of returning True is p and the probability of returning False is 1 - p"
        rnd = random.random()
        if rnd <= p:
            return True
        else:
            return False

    def __init__(self, id, inputSize, outputSize):
        self.id = id
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.fitness = 0
        self.biasNode = Node(id=0, tag='Bias Node', value=1)
        self.nodeCount = 1

        # input node
        self.inputNodes = []
        for i in range(inputSize):
            self.inputNodes.append(Node(id=self.nodeCount, tag='Input Node'))
            self.nodeCount += 1

        # hidden node
        self.hiddenNodes = []

        # output node
        self.outputNodes = []
        for j in range(outputSize):
            self.outputNodes.append(Node(id=self.nodeCount, tag='Output Node'))
            self.nodeCount += 1

        # connection
        self.connections = []
        for i in range(inputSize):
            for j in range(outputSize):
                self.addConnection(self.inputNodes[i], self.outputNodes[j])
        for j in range(outputSize):
            self.addConnection(self.biasNode, self.outputNodes[j])

    def lenConnections(self):
        length = 0
        for con in self.connections:
            if con.enable:
                length += 1
        return length

    def showStructure(self):
        print "Genome %d(fitness = %d):"%(self.id, self.fitness)
        print "\tTotal Nodes:%d\tHidden Nodes:%d"%(self.nodeCount, len(self.hiddenNodes))
        print "\tEnabled Connections(%d):"%self.lenConnections()
        for con in self.connections:
            print "\t\t[%s %d] = %f\t**[%f]**\t[%s %d] = %f\tEnable = %s\tInnovation = %d"%(
                    con.input.tag, con.input.id, con.input.value,
                    con.weight,
                    con.output.tag, con.output.id, con.output.value,
                    con.enable, con.innovation)
        print

    def updateNode(self, id):
        sum = 0
        for con in self.connections:
            if con.enable and con.output.id == id:
                sum += con.input.value * con.weight
        return self.sigmoid(sum)

    def forwardPropagation(self):
        for hid in self.hiddenNodes:
            hid.value = self.updateNode(hid.id)

        for out in self.outputNodes:
            out.value = self.updateNode(out.id)

    @staticmethod
    def getInnovation(connection):
        # check existed connection
        for con in NEAT.connectionList:
            if con == connection:
                return con.innovation
        # new innovation number
        res = len(NEAT.connectionList)
        NEAT.connectionList.append(connection)
        return res

    def addConnection(self, inputNode, outputNode, weight = None):
        if weight == None:
            con = Connection(input=inputNode, output=outputNode)
            con.randomWeight()
            con.innovation = NEAT.getInnovation(con)
        else:
            con = Connection(input=inputNode, output=outputNode, weight=weight)
            con.innovation = NEAT.getInnovation(con)
        self.connections.append(con)

    def addHiddenNode(self, tag):
        node = Node(self.nodeCount, tag=tag)
        self.hiddenNodes.append(node)
        self.nodeCount += 1
        return node

    def isConnectionExist(self, input, output):
        for con in self.connections:
            if input.id == con.input.id and output.id == con.output.id:
                return True
        return False

    def mutation(self):
        if self.probability(0.6):
            # modify connections
            for con in self.connections:
                if self.probability(0.9):
                    # connection weight mutate
                    if self.probability(0.7):
                        # uniformly perturb
                        con.weight += random.uniform(-3, 3)
                    else:
                        # assign a new random weight
                        con.randomWeight()
                elif self.probability(0.03):
                    # add a new node
                    con.enable = False
                    node = self.addHiddenNode("Hidden Node")
                    self.addConnection(con.input, node, 1)
                    self.addConnection(node, con.output, con.weight)

        elif self.probability(0.7):
            # add new connections
            for hid in self.hiddenNodes:
                # search input nodes
                for node in self.inputNodes:
                    if not self.isConnectionExist(node, hid):
                        if self.probability(0.03):
                            self.addConnection(node, hid)
                # search hidden nodes
                for hid2 in self.hiddenNodes:
                    if hid.id != hid2.id and not self.isConnectionExist(hid, hid2):
                        if self.probability(0.03):
                            self.addConnection(hid, hid2)
                # search output nodes
                for node in self.outputNodes:
                    if not self.isConnectionExist(hid, node):
                        if self.probability(0.03):
                            self.addConnection(hid, node)