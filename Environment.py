# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import NEAT
import random
import copy

class Environment(object):
    """This is an ecological environment that can control the propagation of evolutionary neural networks.
    Attributes:
        input_size: The input size of the genomes.
        output_size: The output size of the genomes.
        population_size: The population of genomes in the environment.
        max_generation: The maximum number of genomes generations
        genomes: The list of NEAT(NeuroEvolution of Augmenting Topologies)
    """
    def __init__(self,input_size, output_size, init_population, max_generation):
        self.input_size = input_size
        self.output_size = output_size
        self.population = init_population
        self.max_generation = max_generation
        self.genomes = [NEAT(i, input_size, output_size) for i in range(init_population)]
        self.next_generation = []
        self.outcomes = []
        self.generation_iter = 0
        self.species = [[]]
        self.delta_t = 5

    def produce_offspring(self, genome):
        """Produce a new offspring."""
        offspring = copy.deepcopy(genome)
        offspring.id = self.population
        self.next_generation.append(offspring)
        return offspring

    def add_outcome(self, genome):
        """Collecting outcomes."""
        gen = copy.deepcopy(genome)
        self.outcomes.append(gen)
        # print "Generation:%d\tFound outcome %d,\thidden node = %d,\tconnections = %d"%(self.generation_iter,
        #                                                                                len(self.outcomes),
        #                                                                                len(gen.hidden_nodes),
        #                                                                                gen.connection_count())

    def mating_pair(self, pair):
        """Mating two genomes."""
        p1 = pair[0]
        p2 = pair[1]
        p1_len = len(p1.connections)
        p2_len = len(p2.connections)
        offspring = self.produce_offspring(NEAT(self.population, self.input_size, self.output_size, offspring=True))

        # Generate the same number of nodes as the larger genome
        max_hidden_node = max(len(p1.hidden_nodes), len(p2.hidden_nodes))
        for i in range(max_hidden_node):
            offspring.add_hidden_node()

        # Crossing over
        i, j = 0, 0
        while i < p1_len or j < p2_len:
            if i < p1_len and j < p2_len:
                if p1.connections[i].innovation == p2.connections[j].innovation:
                    if NEAT.probability(0.5):
                        con = p1.connections[i]
                    else:
                        con = p2.connections[j]
                    i += 1
                    j += 1
                elif p1.connections[i].innovation < p2.connections[j].innovation:
                    con = p1.connections[i]
                    i += 1
                else:
                    con = p2.connections[j]
                    j += 1
            elif i >= p1_len:
                con = p2.connections[j]
                j += 1
            else:
                con = p1.connections[i]
                i += 1
            offspring.add_connection_id(input_node_id=con.input.id,
                                        output_node_id=con.output.id,
                                        weight=con.weight,
                                        enable=con.enable)

    def mating_genomes(self):
        """Randomly mating two genomes."""
        mating_pool = []
        for k, gen in enumerate(self.genomes):
            # The higher the fitness, the higher the probability of mating.
            if NEAT.probability(0.2 * (gen.fitness * 2)):
                mating_pool.append(gen)

        while len(mating_pool) > 1:
            pair = random.sample(mating_pool, 2)
            self.mating_pair(pair)
            for p in pair:
                mating_pool.remove(p)

    def mutation(self, task):
        """Genome mutation."""
        for k, gen in enumerate(self.genomes):
            if gen.fitness < task.best_fitness:
                if NEAT.probability(0.2):
                    offspring = self.produce_offspring(gen)
                    offspring.mutation()
                    task.xor_fitness(offspring)
                else:
                    gen.mutation()
                    task.xor_fitness(gen)

    def compatibility(self, gen1, gen2):
        """Calculating compatibility between two genomes."""
        g1_len = len(gen1.connections)
        g2_len = len(gen2.connections)
        E, D = 0, 0
        i, j = 0, 0
        w1, w2 = 0, 0
        while i < g1_len or j < g2_len:
            if i < g1_len and j < g2_len:
                if gen1.connections[i].innovation == gen2.connections[j].innovation:
                    w1 += abs(gen1.connections[i].weight)
                    w2 += abs(gen2.connections[j].weight)
                    i += 1
                    j += 1
                elif gen1.connections[i].innovation < gen2.connections[j].innovation:
                    D += 1
                    w1 += abs(gen1.connections[i].weight)
                    i += 1
                else:
                    D += 1
                    w2 += abs(gen2.connections[j].weight)
                    j += 1
            elif i >= g1_len:
                E += 1
                w2 += abs(gen2.connections[j].weight)
                j += 1
            else:
                E += 1
                w2 += abs(gen1.connections[i].weight)
                i += 1
        W = abs(w1 - w2)
        distance = 0.6 * E + 0.8 * D + 0.1 * W
        return distance

    def speciation(self):
        pass

    def surviving_rule(self):
        """Set the surviving rules."""
        self.genomes.sort(key=lambda NEAT: NEAT.fitness, reverse=True)
        self.genomes = self.genomes[:40] + self.next_generation + [NEAT(i,
                                                                        self.input_size,
                                                                        self.output_size)
                                                                   for i in range(10)]
        self.population = len(self.genomes)

    def run(self, task, showResult=False):
        """Run the environment."""
        print "Running Environment...(Initial population = %d, Maximum generation = %d)"%(self.population, self.max_generation)
        # generational change
        for self.generation_iter in range(self.max_generation):
            self.next_generation = []

            # mating genomes
            self.mating_genomes()

            # mutation
            self.mutation(task)

            # logging outcome information
            outcomes = [gen for gen in self.genomes if gen.fitness == task.best_fitness]
            genome_len = len(self.genomes)
            avg_hid = 0.0
            avg_con = 0.0
            hidden_distribution = [0]
            if genome_len > 0:
                for gen in self.genomes:
                    avg_hid += len(gen.hidden_nodes)
                    avg_con += gen.connection_count()
                    hid = len(gen.hidden_nodes)
                    while hid >= len(hidden_distribution):
                        hidden_distribution.append(0)
                    hidden_distribution[hid] += 1
                avg_hid /= genome_len
                avg_con /= genome_len
            print "Generation %d:\tpopulation = %d,\tAvg Hidden = %f,\tAvg Connection = %f,\toutcome = %d,\thidden node distribution:%s"%(
                self.generation_iter + 1,
                self.population,
                avg_hid,
                avg_con,
                len(outcomes),
                hidden_distribution)

            # killing bad genomes
            self.surviving_rule()

        for gen in self.genomes:
            if gen.fitness == task.best_fitness:
                self.add_outcome(gen)
                # self.genomes[k] = NEAT(gen.id, self.input_size, self.output_size)
        if showResult:
            print "Completed Genomes:"
            self.outcomes.sort(key=lambda NEAT:NEAT.hidden_nodes)
            outcomes_len = len(self.outcomes)
            avg_hid = 0.0
            avg_con = 0.0
            if outcomes_len > 0:
                for gen in self.outcomes:
                    gen.show_structure()
                    avg_hid += len(gen.hidden_nodes)
                    avg_con += gen.connection_count()
                avg_hid /= outcomes_len
                avg_con /= outcomes_len
            print "Population: %d,\tAverage Hidden node = %f,\tAverage Connection = %f"%(self.population, avg_hid, avg_con)

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