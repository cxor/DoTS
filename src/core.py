import test
import sys
import argparse
from simulator import Simulator
import numpy
    

def plot(stats):
    pass

def main():
    args = parse(sys.argv)
    no_simulations = args[0]
    simulator = Simulator(args)
    stats = numpy.array([0,0,0,0,0])
    for _ in range(no_simulations):
        simulator.run()
        stats += simulator.stat()
        simulator.plot()
    stats /= no_simulations
    plot(stats)

if __name__ == "__main__":
    main()