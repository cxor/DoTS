import numpy as np
import math
import matplotlib.pyplot as plt
from map import Map
from node import Node


def main():
    nodes = []
    while len(nodes) < 4:       # Voglio una mappa significativa, no?
        simulation_map = Map(topology="roads", size=[20,10])
        nodes = simulation_map.add_nodes()

    print("Topology: ")
    simulation_map.draw_topology()
    print("\nInitial condition: ")
    for i in range(len(nodes)):
        print(f"\nNode {i}", end="\n")
        print(f"  Start position: {nodes[i].get_start()} - Target waypoint: {nodes[i].get_target()}", end="\n")
        print(f"Path to be followed: {nodes[i].get_path()}")
        # print(str(nodes[i].get_position()))
    simulation_map.draw_with_nodes()
    return


if __name__ == "__main__":
    main()