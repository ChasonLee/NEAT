# NEAT
NeuroEvolution of Augmenting Topologies

## Description
- The code is written according to my own understanding of the paper.
- The project is still in progress.

## Usage
- Solving XOR Problem: ```python TestXOR.py```

```
usage: TestXOR.py [-h] [--pop POP] [--gen GEN] [--thr THR] [--cmp CMP]
                  [--mat MAT] [--cpy CPY] [--slf SLF] [--exc EXC] [--dsj DSJ]
                  [--wgh WGH] [--srv SRV]

Change the evolutionary parameters.

optional arguments:
  -h, --help  show this help message and exit
  --pop POP   The initial population size.
  --gen GEN   The maximum generations.
  --thr THR   The compatibility threshold.
  --cmp CMP   The number of genomes used to compare compatibility.
  --mat MAT   The mating probability.
  --cpy CPY   The copy mutation probability.
  --slf SLF   The self mutation probability.
  --exc EXC   The excess weight.
  --dsj DSJ   The disjoint weight.
  --wgh WGH   The average weight differences weight.
  --srv SRV   The number of survivors per generation.
```

- Playing Tictactoe game: ```python TestTictactoe.py```

## Paper Link
[Evolving Neural Networks through Augmenting Topologies](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
