# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *
import math

class NEAT:
    def __init__(self, inputNum, outputNum):
        self.inputNum = inputNum
        self.outputNum = outputNum
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
        self.connections = []
        for i in range(inputNum):
            for j in range(outputNum):
                self.addConnection(self.inputNodes[i], self.outputNodes[j])

        for j in range(outputNum):
            self.addConnection(self.biasNode, self.outputNodes[j])

    def addConnection(self, inputNode, outputNode, weight = None):
        if weight == None:
            con = Connection(inputNode, outputNode)
            con.randomWeight()
        else:
            con = Connection(inputNode, outputNode, weight)
        self.connections.append(con)


    def showStructure(self):
        print "Total nodes:", self.nodeCount
        print "Connections(%d):"%len(self.connections)
        for con in self.connections:
            print "\t[%s %d] = %f\t**[%f]**\t[%s %d] = %f\tEnable = %s"%(con.input.tag, con.input.id, con.input.value,
                                                                        con.weight,
                                                                        con.output.tag, con.output.id, con.output.value,
                                                                        con.enable )
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
        if random.random() <= p:
            return True
        else:
            return False

    def addHiddenNode(self, tag):
        node = Node(self.nodeCount, tag=tag)
        self.hiddenNodes.append(node)
        self.nodeCount += 1
        return node

    def mutation(self):
        for con in self.connections:
            if self.probability(0.8):
                # connection weight mutate
                if self.probability(0.9):
                    # uniformly perturb
                    con.weight += (random.random() * 2 - 1) * 3
                else:
                    # assign a new random weight
                    con.randomWeight()
            elif self.probability(0.5):
                # add a new node
                con.enable = False
                node = self.addHiddenNode("Hidden Node")
                self.addConnection(con.input, node, 1)
                self.addConnection(node, con.output, con.weight)


