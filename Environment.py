# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import *


class Environment:
    def __init__(self,inputNum, outputNum, populationSize, maxGeneration):
        self.populationSize = populationSize
        self.maxGeneration = maxGeneration
        self.genome = [NEAT(i, inputNum, outputNum) for i in range(populationSize)]
        self.innovation = [(inputNum + 1) * outputNum]

    def matingGenome(self):
        pass

    def run(self):
        for i in range(self.maxGeneration):

            # mutation
            for gen in self.genome:
                gen.mutation(self.innovation)
        for gen in self.genome:
            gen.showStructure()

    def test(self):
        innovation = [3]

        neat = NEAT(0, 2, 1)
        neat.inputNodes[0].value = 1
        neat.inputNodes[1].value = 1
        neat.forwardPropagation()
        neat.showStructure()

        neat.addHiddenNode("hidden node")
        neat.forwardPropagation()
        neat.showStructure()

        neat.mutation(innovation)
        neat.forwardPropagation()
        neat.showStructure()

        neat.mutation(innovation)
        neat.forwardPropagation()
        neat.showStructure()