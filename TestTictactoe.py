# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys
import argparse

class TictactoeTest:
    best_fitness = 100
    input_size = 9*3
    output_size = 9

    @staticmethod
    def tictactoe_fitness(genome):
        fitness = 0
        return fitness

def main(args=None):
    env = Environment(input_size=TictactoeTest.input_size,
                      output_size=TictactoeTest.output_size,
                      init_population=args.pop,
                      max_generation=args.gen,
                      task=TictactoeTest)

    # env.test()
    env.run(task=TictactoeTest, showResult=True)

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
