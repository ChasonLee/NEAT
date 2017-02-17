# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys

class XorTest(object):
    best_fitness = 4
    @staticmethod
    def xor_fitness(genome):
        fitness = 0
        for case in [[[0, 0], [0]], [[0, 1], [1]], [[1, 0], [1]], [[1, 1], [0]]]:
            for i in range(len(genome.input_nodes)):
                genome.input_nodes[i].value = case[0][i]
            genome.forward_propagation()
            for i in range(len(genome.output_nodes)):
                if round(genome.output_nodes[i].value) != case[1][i]:
                    break
            else:
                fitness += 1
        genome.fitness = fitness

def main(argv=None):
    env = Environment(input_size=2, output_size=1, init_population=1000, max_generation=150)

    # env.test()
    env.run(task=XorTest, showResult=True)

if __name__ == "__main__":
    sys.exit(main())