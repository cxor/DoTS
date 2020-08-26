import numpy as np
import math
import matplotlib.pyplot as plt
from map import Map
from node import Node


def main():
    simulation_map = Map(topology="roads", size=[20,10])
    print("Topology: ")
    simulation_map.draw_topology()
    print("\nInitial condition: ")
    nodes = simulation_map.add_nodes()
    for i in range(len(nodes)):
        print(str(nodes[i].get_position()))
    simulation_map.draw_with_nodes()
    return


if __name__ == "__main__":
    main()