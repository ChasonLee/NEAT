# -*- coding: utf-8 -*-
__author__ = 'Chason'

from NEAT import *

neat = NEAT(2, 1)
neat.inputNodes[0].value = 1
neat.inputNodes[1].value = 1
neat.forwardPropagation()
neat.showStructure()

neat.mutation()
neat.forwardPropagation()
neat.showStructure()