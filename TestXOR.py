# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys

class XorTest:
    bestFitness = 4
    @staticmethod
    def XorFitness(genome):
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

def main(argv=None):
    env = Environment(inputNum=2, outputNum=1, populationSize=10000, maxGeneration=200)

    # env.test()
    env.run(task=XorTest, showResult=False)

if __name__ == "__main__":
    sys.exit(main())