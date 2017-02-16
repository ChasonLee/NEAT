# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import NEAT
import random

class Environment(object):
    """This is an ecological environment that can control the propagation of evolutionary neural networks.
    Attributes:
        input_size: The input size of the genomes.
        output_size: The output size of the genomes.
        population_size: The population of genomes in the environment.
        max_generation: The maximum number of genomes generations
        genomes: The list of NEAT(NeuroEvolution of Augmenting Topologies)
    """
    def __init__(self,input_size, output_size, population_size, max_generation):
        self.input_size = input_size
        self.output_size = output_size
        self.population_size = population_size
        self.max_generation = max_generation
        self.genomes = [NEAT(i, input_size, output_size) for i in range(population_size)]
        self.outcomes = []
        self.generation_iter = 0

    def add_outcome(self, genome):
        self.outcomes.append(genome)
        print "Generation:%d\tFound outcome %d,\thidden node = %d,\tconnections = %d"%(self.generation_iter,
                                                                                       len(self.outcomes),
                                                                                       len(genome.hidden_nodes),
                                                                                       genome.connection_count())

    def mating_pair(self, pair):
        p1 = pair[0].connections.sort(key=lambda Connection:Connection.innovation)
        p2 = pair[1].connections.sort(key=lambda Connection:Connection.innovation)
        p1_len = len(p1)
        p2_len = len(p2)
        max_len = max(p1_len, p2_len)
        # to be continue

    def mating_genomes(self):
        mating_pool = []
        for k, gen in enumerate(self.genomes):
            if NEAT.probability(0.01 * gen.fitness):
                mating_pool.append(gen)

        while len(mating_pool) > 0:
            pair = random.sample(mating_pool, 2)
            self.mating_pair(pair)
            for p in pair:
                mating_pool.remove(p)

    def mutation(self, task):
        for k, gen in enumerate(self.genomes):
            gen.mutation()
            task.xor_fitness(gen)
            # collecting outcomes
            if gen.fitness == task.best_fitness:
                self.add_outcome(gen)
                self.genomes[k] = NEAT(gen.id, self.input_size, self.output_size)

    def kill_bad_genomes(self):
        for k, gen in enumerate(self.genomes):
            if gen.fitness <= 1 and len(gen.hidden_nodes) > 1:
                self.genomes[k] = NEAT(gen.id, self.input_size, self.output_size)

    def run(self, task, showResult=False):
        """Run the environment."""
        print "Running Environment...(population size = %d, max generation = %d)"%(self.population_size, self.max_generation)
        # generational change
        for self.generation_iter in range(self.max_generation):

            # mutation
            self.mutation(task)

            # killing bad genomes
            self.kill_bad_genomes()

        if showResult:
            print "Completed Genomes:"
            self.outcomes.sort(key=lambda NEAT:NEAT.hidden_nodes)
            for gen in self.outcomes:
                gen.show_structure()

    @staticmethod
    def test():
        neat = NEAT(0, 2, 1)
        neat.input_nodes[0].value = 1
        neat.input_nodes[1].value = 1
        neat.forward_propagation()
        neat.show_structure()

        neat.add_hidden_node()
        neat.forward_propagation()
        neat.show_structure()

        neat.mutation()
        neat.forward_propagation()
        neat.show_structure()

        neat.mutation()
        neat.forward_propagation()
        neat.show_structure()