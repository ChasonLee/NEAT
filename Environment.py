# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import *
import copy

class Environment:
    def __init__(self,inputNum, outputNum, populationSize, maxGeneration):
        self.inputNum = inputNum
        self.outputNum = outputNum
        self.populationSize = populationSize
        self.maxGeneration = maxGeneration
        self.genomes = [NEAT(i, inputNum, outputNum) for i in range(populationSize)]
        self.innovation = [(inputNum + 1) * outputNum]

    def matingGenome(self):
        pass

    def run(self, task, showResult=False):
        print "Running Environment..."
        for i in range(self.maxGeneration):
            # mutation
            for gen in self.genomes:
                gen.mutation(self.innovation)
                task.XorFitness(gen)
                if  gen.fitness == task.bestFitness:
                    fitness = gen.fitness
                    print "best fitness:", fitness
                    gen.showStructure()
            # killing bad genomes
            for k, gen in enumerate(self.genomes):
                if gen.fitness <= 1 and len(gen.hiddenNodes) > 0:
                    self.genomes[k] = NEAT(gen.id, self.inputNum, self.outputNum)
        if showResult:
            bestFitness = 0
            maxHiddenNodes = 0
            for gen in self.genomes:
                gen.showStructure()
                if bestFitness < gen.fitness:
                    bestFitness = gen.fitness
                if maxHiddenNodes < len(gen.hiddenNodes):
                    maxHiddenNodes = len(gen.hiddenNodes)
            print "Best fitness = %d"%bestFitness
            print "Max hidden nodes = %d"%maxHiddenNodes

    @staticmethod
    def test():
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