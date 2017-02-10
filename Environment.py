# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import NEAT

class Environment:



    def __init__(self,inputSize, outputSize, populationSize, maxGeneration):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.populationSize = populationSize
        self.maxGeneration = maxGeneration
        self.genomes = [NEAT(i, inputSize, outputSize) for i in range(populationSize)]
        self.innovation = [(inputSize + 1) * outputSize]

    def matingGenome(self):
        pass

    def run(self, task, showResult=False):
        print "Running Environment..."
        completedGenomes = []
        for i in range(self.maxGeneration):
            # mutation
            for gen in self.genomes:
                gen.mutation()
                task.XorFitness(gen)
                if  gen.fitness == task.bestFitness:
                    gen.showStructure()
                    completedGenomes.append(gen)
            # killing bad genomes
            for k, gen in enumerate(self.genomes):
                if gen.fitness <= 1 and len(gen.hiddenNodes) > 1:
                    self.genomes[k] = NEAT(gen.id, self.inputSize, self.outputSize)
        if showResult:
            maxHiddenNodes = 0
            print "Completed Genomes:"
            for gen in completedGenomes:
                gen.showStructure()
                if maxHiddenNodes < len(gen.hiddenNodes):
                    maxHiddenNodes = len(gen.hiddenNodes)
            print "Max hidden nodes = %d"%maxHiddenNodes

    @staticmethod
    def test():

        neat = NEAT(0, 2, 1)
        neat.inputNodes[0].value = 1
        neat.inputNodes[1].value = 1
        neat.forwardPropagation()
        neat.showStructure()

        neat.addHiddenNode("hidden node")
        neat.forwardPropagation()
        neat.showStructure()

        neat.mutation()
        neat.forwardPropagation()
        neat.showStructure()

        neat.mutation()
        neat.forwardPropagation()
        neat.showStructure()