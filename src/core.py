import test
import sys
import argparse
from simulator import Simulator
import numpy


def parse(sim_data):
    #print(sim_data)
    param_file = open(sim_data, "r")
    data_lines = param_file.readlines()
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
    for line in data_lines:
        if line.startswith("--run "):
            no_epochs = int(line.lstrip("--run "))
        elif line.startswith("--nodes "):
            nodes = (line.lstrip("--nodes ")).split(" ")
            no_nodes = [int(n) for n in nodes]
            if(len(no_nodes) != no_epochs):
                print(f"--nodes - Error: {no_epochs} parameters expected, but {len(no_nodes)} given")
                break
        elif line.startswith("--sinks "):
            sinks = (line.lstrip("--sinks ")).split(" ")
            no_sinks = [int(s) for s in sinks]
            if(len(no_sinks) != no_epochs):
                print(f"--sinks - Error: {no_epochs} parameters expected, but {len(no_sinks)} given")
                break
        elif line.startswith("--sinksignal "):
            ssignal = (line.lstrip("--sinksignal ")).split(" ")
            sink_signal = [float(s) for s in ssignal]
            if(len(sink_signal) != no_epochs):
                print(f"--sinksignal - Error: {no_epochs} parameters expected, but {len(sink_signal)} given")
                break
        elif line.startswith("--nodespeed "):
            nodespeed = (line.lstrip("--nodespeed ")).split(" ")
            node_speed = [int(n) for n in nodespeed]
            if(len(node_speed) != no_epochs):
                print(f"--nodespeed - Error: {no_epochs} parameters expected, but {len(node_speed)} given")
                break
        elif line.startswith("--nodesignal "):
            nodesignal = (line.lstrip("--nodesignal ")).split(" ")
            node_signal = [float(n) for n in nodesignal]
            if(len(node_signal) != no_epochs):
                print(f"--nodesignal - Error: {no_epochs} parameters expected, but {len(node_signal)} given")
                break
        elif line.startswith("--trxrate "):
            trxrate = (line.lstrip("--trxrate ")).split(" ")
            trx_rate = [float(t) for t in trxrate]
            if(len(trx_rate) != no_epochs):
                print(f"--trxrate - Error: {no_epochs} parameters expected, but {len(trx_rate)} given")
                break
        elif line.startswith("--fault "):
            flt = (line.lstrip("--fault ")).split(" ")
            fault = [float(f) for f in flt]
            if(len(fault) != no_epochs):
                print(f"--fault - Error: {no_epochs} parameters expected, but {len(fault)} given")
                break
        elif line.startswith("--disaster "):
            dis = (line.lstrip("--disaster ")).split(" ")
            disaster = [float(d) for d in dis]
            if(len(disaster) != no_epochs):
                print(f"--disaster - Error: {no_epochs} parameters expected, but {len(disaster)} given")
                break
        elif line.startswith("--mapsize "):
            sizes = (line.lstrip("--mapsize ")).split(" ")
            map_size = [int(s) for s in sizes]
            if(len(map_size) != 2):
                print(f"--disaster - Error: {2} parameters expected, but {len(map_size)} given")
                break
        elif line.startswith("--duration "):
            duration = int(line.lstrip("--duration "))
    print(f"Number of epochs: {no_epochs}")
    print(f"Nodes for each epoch: {no_nodes}")
    print(f"Sinks for each epoch: {no_sinks}")
    print(f"Sink signal for each epoch: {sink_signal}")
    print(f"Node signal for each epoch: {node_signal}")
    print(f"Node speed for each epoch: {node_speed}")
    print(f"Trx rate for each epoch: {trx_rate}")
    print(f"Fault chance for each epoch: {fault}")
    print(f"Disaster chance for each epoch: {disaster}")
    print(f"Map size: {map_size[0]} {map_size[1]}")
    print(f"Epochs' duration: {duration}")
    args = (no_epochs, no_nodes, no_sinks, node_signal, sink_signal, node_speed, fault, disaster, map_size, trx_rate, duration)
    return args 
    

def plot(stats):
    pass

def main():
    if(len(sys.argv) == 2):
        args = parse(sys.argv[1])
    else:
        print("Usage: python core.py sim_data.txt")
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