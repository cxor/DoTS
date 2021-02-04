import numpy as np
import math
import matplotlib.pyplot as plt
from map import Map
from node import Node
from waypoint import Waypoint
import time
import itertools


def main():
    nodes = []
    while len(nodes) < 4:       # Voglio una mappa significativa, no?
        simulation_map = Map(topology="roads", size=[20,10])
        nodes = simulation_map.add_nodes()
        sinks = simulation_map.add_sinks()

    print(sinks)
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
    # by using t as time unit, the while loop iterates
    # through the points (coordinates) that compose the
    # path that each node has to repeatedly walk on 
    # that same path was decided at the beginning, during the 
    # generation of the map.
    # At each "clock" (each iteration) the nodes take one step
    # upon their path (thanks to the modulus operation with t)
    # and continue to go back and forth as long as we want (duration of the while loop)
    # obviously in order to move the nodes we must update the
    # status of the cell in the topology (lines where .topology is called)
    
    #fare un check se due nodi hanno la stessa posizione, in quel caso scambiare il messaggio
    
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
        for a, b in itertools.combinations(nodes, 2):
            if a.get_position() == b.get_position():
                a.exchange_message(b)
                
        for node in nodes:
            for sink in sinks:
                if node.get_position() == sink.get_position():
                    print("Sink and node on the same position")
                    
        print(f"Time = {t}")
        #print(chr(27) + "[2J") # escape sequence that clears the screen in linux terminal so that the drawing looks like it is updating itself
        simulation_map.draw_with_nodes()
        time.sleep(1)
    
    for node in nodes:
        print(str(node) + "received " + str(node.get_received_packet()) + " not received " + str(node.get_not_received_packet()))
        print("\n")
    
    return

    


if __name__ == "__main__":
    main()