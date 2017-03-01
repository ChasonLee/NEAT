# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys
import argparse

class XorTest(object):
    best_fitness = 4
    input_size = 2
    output_size = 1
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

def main(args=None):
    env = Environment(input_size=XorTest.input_size,
                      output_size=XorTest.output_size,
                      init_population=args.pop,
                      max_generation=args.gen)

    # env.test()
    env.run(task=XorTest, showResult=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Change the environment parameters.')
    parser.add_argument(
        '--pop',
        default=150,
        type=int,
        help='The initial population size.'
    )
    parser.add_argument(
        '--gen',
        default=100,
        type=int,
        help='The maximum generations.'
    )
    args = parser.parse_args()
    sys.exit(main(args))