# -*- coding: utf-8 -*-
__author__ = 'Chason'
from Node import *
from Connection import *
# from Environment import Environment

import math

class NEAT(object):
    """An evolutionary neural network called 'NeuroEvolution of Augmenting Topologies(NEAT)'
    Attributes:
        id: The unique identification number of NEAT.
        input_size: Input size of NEAT.
        output_size: Output size of NEAT.
        fitness: Adaptability of NEAT in the environment.
        node_count: The total number of nodes in NEAT.
        bias_node: Bias node in NEAT.
        input_nodes: Input nodes in NEAT.
        hidden_nodes: Hidden nodes in NEAT.
        output_nodes: Output nodes in NEAT.
        connections: Connections in NEAT.
        connection_list(static): A list of all different connections.
    """
    connection_list = []
    @staticmethod
    def sigmoid(z):
        """"Sigmoid activate function"""
        return 1.0 / (1.0 + math.exp(-z))

    @staticmethod
    def tanh(z):
        """"Tanh activate function"""
        return (math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z))

    @staticmethod
    def probability(p):
        """Input range:0 <= p <= 1;The probability of returning True is p, and False is 1 - p"""
        return random.random() <= p

    def __init__(self, id, input_size, output_size):
        self.id = id
        self.input_size = input_size
        self.output_size = output_size
        self.fitness = 0
        self.node_count = 1
        self.bias_node = Node(id=0, tag='Bias Node', value=1)

        # input node
        self.input_nodes = []
        for i in range(input_size):
            self.input_nodes.append(Node(id=self.node_count, tag='Input Node'))
            self.node_count += 1

        # hidden node
        self.hidden_nodes = []

        # output node
        self.output_nodes = []
        for j in range(output_size):
            self.output_nodes.append(Node(id=self.node_count, tag='Output Node'))
            self.node_count += 1

        # connection
        self.connections = []
        for i in range(input_size):
            for j in range(output_size):
                self.add_connection(self.input_nodes[i], self.output_nodes[j])
        for j in range(output_size):
            self.add_connection(self.bias_node, self.output_nodes[j])

    def connection_count(self):
        """Counts the number of connections enabled in NEAT."""
        count = 0
        for con in self.connections:
            if con.enable:
                count += 1
        return count

    def show_structure(self):
        print "Genome %d(fitness = %d):"%(self.id, self.fitness)
        print "\tTotal Nodes:%d\tHidden Nodes:%d"%(self.node_count, len(self.hidden_nodes))
        print "\tEnabled Connections(%d):"%self.connection_count()
        for con in self.connections:
            print "\t\t[%s %d] = %f\t**[%f]**\t[%s %d] = %f\tEnable = %s\tInnovation = %d"%(
                    con.input.tag, con.input.id, con.input.value,
                    con.weight,
                    con.output.tag, con.output.id, con.output.value,
                    con.enable, con.innovation)
        print

    def update_node(self, id):
        """Use sigmoid function to compute node values, ignoring the connections that are not enabled."""
        sum = 0
        for con in self.connections:
            if con.enable and con.output.id == id:
                sum += con.input.value * con.weight
        return self.sigmoid(sum)

    def forward_propagation(self):
        for hid in self.hidden_nodes:
            hid.value = self.update_node(hid.id)

        for out in self.output_nodes:
            out.value = self.update_node(out.id)

    @staticmethod
    def get_innovation(connection):
        """Get innovation number and ensure that the same connection structure has the same innovation number."""
        # check existed connection
        for con in NEAT.connection_list:
            if con == connection:
                return con.innovation
        # new innovation number
        res = len(NEAT.connection_list)
        NEAT.connection_list.append(connection)
        return res

    def add_connection(self, inputNode, outputNode, weight = None):
        """Add a new connection. If the weights are not set, the weights are set at random."""
        if weight == None:
            con = Connection(input=inputNode, output=outputNode)
            con.random_weight()
            con.innovation = NEAT.get_innovation(con)
        else:
            con = Connection(input=inputNode, output=outputNode, weight=weight)
            con.innovation = NEAT.get_innovation(con)
        self.connections.append(con)

    def add_hidden_node(self, tag="Hidden Node"):
        """Add a new hidden node. The default tag is 'Hidden Node'."""
        node = Node(self.node_count, tag=tag)
        self.hidden_nodes.append(node)
        self.node_count += 1
        return node

    def does_connection_exist(self, input, output):
        """Returns true if the connection already exists, otherwise returns false."""
        for con in self.connections:
            if input.id == con.input.id and output.id == con.output.id:
                return True
        return False

    def mutation(self):
        """Let the neural network randomly mutate."""
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
                        con.random_weight()
                elif self.probability(0.03):
                    # add a new node
                    con.enable = False
                    node = self.add_hidden_node()
                    self.add_connection(con.input, node, 1)
                    self.add_connection(node, con.output, con.weight)

        elif self.probability(0.7):
            # add new connections
            new_con_pro = 0.03
            for hid in self.hidden_nodes:
                # consider bias node
                if not self.does_connection_exist(self.bias_node, hid):
                    if self.probability(new_con_pro):
                        self.add_connection(self.bias_node, hid)
                # search input nodes
                for node in self.input_nodes:
                    if not self.does_connection_exist(node, hid):
                        if self.probability(new_con_pro):
                            self.add_connection(node, hid)
                # search hidden nodes
                for hid2 in self.hidden_nodes:
                    if hid.id != hid2.id and not self.does_connection_exist(hid, hid2):
                        if self.probability(new_con_pro):
                            self.add_connection(hid, hid2)
                # search output nodes
                for node in self.output_nodes:
                    if not self.does_connection_exist(hid, node):
                        if self.probability(new_con_pro):
                            self.add_connection(hid, node)