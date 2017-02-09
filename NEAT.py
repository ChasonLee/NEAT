# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *
import math

class NEAT:
    def __init__(self, id, inputNum, outputNum):
        self.id = id
        self.inputNum = inputNum
        self.outputNum = outputNum
        self.fitness = 0
        self.biasNode = Node(id=0, tag='Bias Node', value=1)
        self.nodeCount = 1

        # input node
        self.inputNodes = []
        for i in range(inputNum):
            self.inputNodes.append(Node(id=self.nodeCount, tag='Input Node'))
            self.nodeCount += 1

        # hidden node
        self.hiddenNodes = []

        # output node
        self.outputNodes = []
        for j in range(outputNum):
            self.outputNodes.append(Node(id=self.nodeCount, tag='Output Node'))
            self.nodeCount += 1

        # connection
        innovation = 0
        self.connections = []
        for i in range(inputNum):
            for j in range(outputNum):
                self.addConnection(innovation, self.inputNodes[i], self.outputNodes[j])
                innovation += 1

        for j in range(outputNum):
            self.addConnection(innovation, self.biasNode, self.outputNodes[j])
            innovation += 1

    def addConnection(self, innovation, inputNode, outputNode, weight = None):
        if weight == None:
            con = Connection(innovation, inputNode, outputNode)
            con.randomWeight()
        else:
            con = Connection(innovation, inputNode, outputNode, weight)
        self.connections.append(con)


    def showStructure(self):
        print "Genome %d(fitness = %d):"%(self.id, self.fitness)
        print "\tTotal Nodes:%d\tHidden Nodes:%d"%(self.nodeCount, len(self.hiddenNodes))
        print "\tConnections(%d):"%len(self.connections)
        for con in self.connections:
            print "\t\t[%s %d] = %f\t**[%f]**\t[%s %d] = %f\tEnable = %s\tInnovation = %d"%(
                    con.input.tag, con.input.id, con.input.value,
                    con.weight,
                    con.output.tag, con.output.id, con.output.value,
                    con.enable, con.innovation)
        print

    def sigmoid(self, z):
        return 1.0 / (1.0 + math.exp(-z))

    def tanh(self, z):
        return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

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

    def probability(self, p):
        rnd = random.random()
        if rnd <= p:
            return True
        else:
            return False

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

    def mutation(self, innovation):
        if self.probability(0.6):
            # modify connections
            for con in self.connections:
                if self.probability(0.9):
                    # connection weight mutate
                    if self.probability(0.9):
                        # uniformly perturb
                        con.weight += random.uniform(-2, 2)
                    else:
                        # assign a new random weight
                        con.randomWeight()
                elif self.probability(0.05):
                    # add a new node
                    con.enable = False
                    node = self.addHiddenNode("Hidden Node")
                    self.addConnection(innovation[0], con.input, node, 1)
                    innovation[0] += 1
                    self.addConnection(innovation[0], node, con.output, con.weight)
                    innovation[0] += 1
        else:
            # add new connections
            for hid in self.hiddenNodes:
                # search input nodes
                for node in self.inputNodes:
                    if not self.isConnectionExist(node, hid):
                        if self.probability(0.05):
                            self.addConnection(innovation[0], node, hid)
                            innovation[0] += 1
                # search hidden nodes
                for hid2 in self.hiddenNodes:
                    if hid.id != hid2.id and not self.isConnectionExist(hid, hid2):
                        if self.probability(0.05):
                            self.addConnection(innovation[0], hid, hid2)
                            innovation[0] += 1
                # search output nodes
                for node in self.outputNodes:
                    if not self.isConnectionExist(hid, node):
                        if self.probability(0.05):
                            self.addConnection(innovation[0], hid, node)
                            innovation[0] += 1
