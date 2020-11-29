import numpy as np
import math
import matplotlib.pyplot as plt
from map import Map
from node import Node
from waypoint import Waypoint


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
    # return

    # Now I try to get the nodes moving
    t = -1 # time unit
    while(t<30):
        print("\n")
        t = t+1
        for node in nodes:
            path_len = len(node.get_path())
            old_coords = node.get_position()
            simulation_map.topology[old_coords[0]][old_coords[1]].set_status(1)
            new_coords = node.get_path()[t%path_len]
            node.set_position(new_coords)
            print(f"Node was in {old_coords} and now goes in {new_coords}")
            simulation_map.topology[new_coords[0]][new_coords[1]].set_status(2)
        print(f"Time = {t}")
        simulation_map.draw_with_nodes()
    return


if __name__ == "__main__":
    main()