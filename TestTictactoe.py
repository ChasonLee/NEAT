# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys
import argparse

class TictactoeTest:
    play_times = 1000
    best_fitness = 2 * play_times
    player = 1
    ROW = 3
    COL = 3
    WIN_NUM = 3
    DRAW = 3
    input_size = ROW * COL * 3
    output_size = ROW * COL
    board = []
    turns = 0

    def judge(self, loc):
        player = self.board[loc]
        r = loc / self.COL
        c = loc % self.COL
        for dr, dc in [[-1, -1], [-1, 0], [-1, 1], [0, 1]]:
            nr = r + dr
            nc = c + dc
            count = 1
            while nr >= 0 and nr < self.ROW and nc >= 0 and nc < self.COL:
                if self.board[nr * self.COL + nc] == player:
                    count = count + 1
                    nr = nr + dr
                    nc = nc + dc
                else:
                    break
            dr = -dr
            dc = -dc
            nr = r + dr
            nc = c + dc
            while nr >= 0 and nr < self.ROW and nc >= 0 and nc < self.COL:
                if self.board[nr * self.COL + nc] == player:
                    count = count + 1
                    nr = nr + dr
                    nc = nc + dc
                else:
                    break
            if count >= self.WIN_NUM:
                return player

        if self.turns >= self.ROW * self.COL:
            return self.DRAW
        return None
    def tictactoe_fitness(self, genome):
        fitness = 0
        for i in range(self.play_times):
            pass
        return fitness

def main(args=None):
    env = Environment(input_size=TictactoeTest.input_size,
                      output_size=TictactoeTest.output_size,
                      init_population=args.pop,
                      max_generation=args.gen,
                      comp_threshold=args.thr,
                      avg_comp_num=args.cmp,
                      mating_prob=args.mat,
                      copy_mutate_pro=args.cpy,
                      self_mutate_pro=args.slf,
                      excess=args.exc,
                      disjoint=args.dsj,
                      weight=args.wgh,
                      survive=args.srv,
                      task=TictactoeTest())

    # env.test()
    env.run(task=TictactoeTest(), showResult=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Change the evolutionary parameters.')
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
    parser.add_argument(
        '--thr',
        default=1.5,
        type=float,
        help='The compatibility threshold.'
    )
    parser.add_argument(
        '--cmp',
        default=50,
        type=int,
        help='The number of genomes used to compare compatibility.'
    )
    parser.add_argument(
        '--mat',
        default=0.6,
        type=float,
        help='The mating probability.'
    )
    parser.add_argument(
        '--cpy',
        default=0.1,
        type=float,
        help='The copy mutation probability.'
    )
    parser.add_argument(
        '--slf',
        default=0.99,
        type=float,
        help='The self mutation probability.'
    )
    parser.add_argument(
        '--exc',
        default=0.9,
        type=float,
        help='The excess weight.'
    )
    parser.add_argument(
        '--dsj',
        default=0.1,
        type=float,
        help='The disjoint weight.'
    )
    parser.add_argument(
        '--wgh',
        default=0.001,
        type=float,
        help='The average weight differences weight.'
    )
    parser.add_argument(
        '--srv',
        default=15,
        type=int,
        help='The number of survivors per generation.'
    )
    args = parser.parse_args()
    sys.exit(main(args))
