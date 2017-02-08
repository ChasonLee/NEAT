# -*- coding: utf-8 -*-
__author__ = 'Chason'
import random

class Connection:
    def __init__(self, input, output, weight = None, enable = True):
        self.input = input
        self.output = output
        if weight != None:
            self.weight = weight
        else:
            self.weight = self.randomWeight()
        self.enable = enable

    def randomWeight(self):
        self.weight = (random.random() * 2 - 1) * 10