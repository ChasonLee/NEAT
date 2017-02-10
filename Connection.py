# -*- coding: utf-8 -*-
__author__ = 'Chason'
import random

class Connection:
    def __init__(self, input, output, weight = None, innovation = None, enable = True):
        self.input = input
        self.output = output
        if weight != None:
            self.weight = weight
        else:
            self.weight = self.randomWeight()
        self.enable = enable
        self.innovation = innovation

    def __eq__(self, other):
        return self.input == other.input and self.output == other.output

    def randomWeight(self):
        self.weight = random.uniform(-10, 10)