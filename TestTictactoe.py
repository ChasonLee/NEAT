# -*- coding: utf-8 -*-
__author__ = 'Chason'

from Environment import *
import sys
import argparse

class TictactoeTest:
    play_times = 1000
    best_fitness = play_times
    player = 1
    ROW = 3
    COL = 3
    WIN_NUM = 3
    DRAW = 3
    input_size = ROW * COL * 3
    output_size = 9
    board = []
    turns = 0
    def judge(self, loc):
        player = self.board[loc]
        r = loc / self.COL
        c = loc % self.COL
        for i in range(4):
            if i == 0:
                dr = -1
                dc = -1
            elif i == 1:
                dr = -1
                dc = 0
            elif i == 2:
                dr = -1
                dc = 1
            else:
                dr = 0
                dc = 1
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
        default=1000,
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
