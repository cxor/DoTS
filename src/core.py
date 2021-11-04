import test
import sys
import argparse
from simulator import Simulator
import numpy


def parse():
    no_epochs = 0
    no_nodes = []
    no_sinks = []
    node_speed = []
    trx_rate = []
    fault = []
    disaster = []
    map_size = []
    duration = []
    node_signal = []
    sink_signal = []

    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=int, dest='no_epochs', help="number of epochs to run")
    parser.add_argument("--nodes", type=int, nargs=no_epochs, help="number of nodes for each epoch")
    parser.add_argument("--sinks", type=int, nargs=no_epochs, help="number of sinks for each epoch") # --sinks 10 20 100
    parser.add_argument("--node-speed", type=int, nargs=no_epochs, help="speed of nodes for each epoch")
    parser.add_argument("--node-signal", type=float, nargs=no_epochs, help="signal strength of nodes for each epoch")
    parser.add_argument("--sink-signal", type=float, nargs=no_epochs, help="signal strength of sinks for each epoch")
    parser.add_argument("--trx-rate", type=float, nargs=no_epochs, help="transmission rate for each epoch")
    parser.add_argument("--fault", type=float, nargs=no_epochs, help="fault for each epoch")
    parser.add_argument("--disaster", type=float, nargs=no_epochs, help="disaster for each epoch")
    parser.add_argument("--map-size", type=int, nargs=2, help="size of the map")
    parser.add_argument("--duration", type=int, help="duration for each epoch")
    args = parser.parse_args()

    

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