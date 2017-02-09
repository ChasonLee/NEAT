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

    def calcFitness(self, genome):
        fitness = 0
        for case in [[[0, 0], [0]], [[0, 1], [1]], [[1, 0], [1]], [[1, 1], [0]]]:
            for i in range(len(genome.inputNodes)):
                genome.inputNodes[i].value = case[0][i]
            genome.forwardPropagation()
            for i in range(len(genome.outputNodes)):
                if round(genome.outputNodes[i].value) != case[1][i]:
                    break
            else:
                fitness += 1
        genome.fitness = fitness

    def run(self):
        fitness = 0
        for i in range(self.maxGeneration):
            # mutation
            for gen in self.genomes:
                gen.mutation(self.innovation)
                self.calcFitness(gen)
                if gen.fitness > fitness or gen.fitness == 4:
                    fitness = gen.fitness
                    print "best fitness:", fitness
                    gen.showStructure()

            for k, gen in enumerate(self.genomes):
                if gen.fitness < 2:
                    self.genomes[k] = NEAT(gen.id, self.inputNum, self.outputNum)

        # for gen in self.genomes:
        #     gen.showStructure()
        # print "best fitness:", fitness

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