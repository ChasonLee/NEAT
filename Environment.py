# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import NEAT

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

    def mating_genomes(self):
        pass

    def run(self, task, showResult=False):
        """Run the environment."""
        print "Running Environment..."
        completed_genomes = []
        for i in range(self.max_generation):
            # mutation
            for gen in self.genomes:
                gen.mutation()
                task.xor_fitness(gen)
                if  gen.fitness == task.best_fitness:
                    gen.show_structure()
                    completed_genomes.append(gen)
            # killing bad genomes
            for k, gen in enumerate(self.genomes):
                if gen.fitness <= 1 and len(gen.hidden_nodes) > 1:
                    self.genomes[k] = NEAT(gen.id, self.input_size, self.output_size)
        if showResult:
            max_hidden_nodes = 0
            print "Completed Genomes:"
            for gen in completed_genomes:
                gen.show_structure()
                if max_hidden_nodes < len(gen.hidden_nodes):
                    max_hidden_nodes = len(gen.hidden_nodes)
            print "Max hidden nodes = %d"%max_hidden_nodes

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