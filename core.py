import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from map import Map
from node import Node
from waypoint import Waypoint
import time
import itertools
import random


def prepare_map():
    nodes = []
    sinks = []
    
    #while len(nodes) < 11 and len(sinks) < 3:       # Voglio una mappa significativa, no?
    while len(nodes) < 11 and len(sinks)<3:       # Voglio una mappa significativa, no?
        while len(sinks) < 3:
            simulation_map = Map(topology="roads", size=[20,10])
            sinks = simulation_map.add_sinks()
        nodes = simulation_map.add_nodes(sinks)
    
    return simulation_map, sinks, nodes


def insinkarea(n, s, s_power=1):
    lat_n = n.get_position()[0]
    lat_s = s.get_position()[0]
    lon_n = n.get_position()[1]
    lon_s = s.get_position()[1]
    lat_low = lat_s - s_power
    lat_high = lat_s + s_power
    lon_low = lon_s - s_power
    lon_high = lon_s + s_power
    if(lat_low <= lat_n <= lat_high):
        if(lon_low <= lon_n <= lon_high):
            return True
    return False    


def execute_simulation(sim_map, param_sinks, param_nodes, crash_nodes = 0, disaster = False, n_sim=0):
    simulation_map = sim_map
    nodes = param_nodes
    sinks = param_sinks
    
    total_nodes_packets_generated = 0
    total_nodes_packets_transferred = 0
    total_nodes_packets_lost = 0
    total_sinks_packets_received = 0
    total_sinks_packets_lost = 0
    summation_nodes_speed = 0
    summation_nodes_gen_rates = 0

    traffic_nodes = []
    traffic_sinks = []
    lost_traffic_nodes = []
    lost_traffic_sinks = []
    sinks_fullness = []

    will_crash = random.sample(range(len(nodes)), crash_nodes)
    moment_crash = random.sample(range(20,55), crash_nodes)
    moment_crash.sort()
    #print(sinks)
    print("Topology: ")
    simulation_map.draw_topology()
    print("\nInitial condition: ")
    for i in range(len(nodes)):
        print(f"\nNode {i}", end="\n")
        print(f"  Start position: {nodes[i].get_start()} - Target waypoint: {nodes[i].get_target()}", end="\n")
        print(f"Path to be followed: {nodes[i].get_path()}")
    simulation_map.draw_with_nodes()

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

    pkts_generated_per_t = []

    t = -1 # time unit
    while(t<59):
        t = t+1
        crash_it = False
        if(len(moment_crash)!=0):
            if t==moment_crash[0]:
                crash_it = True
                tmp = moment_crash[0]
                moment_crash.remove(tmp)
        print("\n")
        tmp_traffic_nodes = 0
        tmp_lost_traffic_nodes = 0
        tmp_traffic_sinks = 0
        tmp_lost_traffic_sinks = 0
        total_n_gen = 0
        
        for node in nodes:
            if(node.get_active() and crash_it and (node.get_id() in will_crash)):
                print("NODE ", str(node.get_id()) ," CRASHED")
                node.set_active(ac=False)
                old_coords = node.get_position()
                simulation_map.topology[old_coords[0]][old_coords[1]].set_status(5)
                crash_it = False
            if(node.get_active()):
                path_len = len(node.get_path())
                old_coords = node.get_position()
                for s in sinks:
                    if s.get_position()==old_coords:
                        simulation_map.topology[old_coords[0]][old_coords[1]].set_status(3)
                    else:
                        simulation_map.topology[old_coords[0]][old_coords[1]].set_status(1)
                s = node.get_speed()
                index_new_pos = int((s / 60) * t)       # since nodes have a speed, I make them change "area" in the map according to that
                new_coords = node.get_path()[index_new_pos%path_len]
                # new_coords = node.get_path()[t%path_len]
                node.set_position(new_coords)
                old_n_gen = node.n_packets_generated
                node.generate_packets()
                new_n_gen = node.n_packets_generated
                diff_n_gen = new_n_gen - old_n_gen
                print(f"Node {node.get_id()} was in {old_coords} and now goes in {new_coords}")
                simulation_map.topology[new_coords[0]][new_coords[1]].set_status(2)
                total_n_gen += diff_n_gen
        
        pkts_generated_per_t.append(total_n_gen)

        for a, b in itertools.combinations(nodes, 2):
            if (a.get_position() == b.get_position() and a.get_active() and b.get_active()):
                a.exchange_message(b)
                b.exchange_message(a)
                tmp_traffic_nodes += (a.n_packets_sent + b.n_packets_sent) # amounts of pkt data constituting "valid" traffic in this time unit
                tmp_lost_traffic_nodes += (a.n_packets_not_sent + b.n_packets_not_sent)
        traffic_nodes.append(tmp_traffic_nodes)
        lost_traffic_nodes.append(tmp_lost_traffic_nodes)
                
        for node in nodes:
            for sink in sinks:
                #if (node.get_position() == sink.get_position() and node.get_active()):
                if (insinkarea(node, sink) and node.get_active()):
                    sink.message_exchange(node)
                    print("Sink and node on the same position")
                    tmp_traffic_sinks += sink.n_packets_received
                    tmp_lost_traffic_sinks += sink.n_packets_not_received
        traffic_sinks.append(tmp_traffic_sinks)
        lost_traffic_sinks.append(tmp_lost_traffic_sinks)

        sinks_pkts = []
        for i in range(len(sinks)):
            sinks_pkts.append(0)
        for sink in sinks:
            s_ind = sink.get_id()
            sinks_pkts[s_ind] = sink.n_packets_received
        sinks_fullness.append(sinks_pkts)
                    
        print(f"Time = {t}")
        #print(chr(27) + "[2J") # escape sequence that clears the screen in linux terminal so that the drawing looks like it is updating itself
        img = simulation_map.draw_with_nodes() # we can think about "animating" it via colormap below
        #plt.imshow(img, interpolation='none')
        #plt.show(block=False)
        #plt.pause(0.6)
        #plt.close()

    for node in nodes:
        summation_nodes_speed += node.get_speed()
        summation_nodes_gen_rates += node.get_rate()
        total_nodes_packets_generated += node.n_packets_generated
        total_nodes_packets_transferred += node.n_packets_received
        total_nodes_packets_lost += node.n_packets_not_received
        #print(str(node) + "received " + str(node.get_n_received_packet()) + " not received " + str(node.get_n_not_received_packet()))
        #print(str(node) + "total packets generated : " + str(node.n_packets_generated))
        #print(str(node) + "queue packet gen :" +str(node.packets_generated.queue))
        #print(str(node) + "queue packet rec :" +str(node.packets_received.queue))
        print("\n")
        
    for sink in sinks:
        total_sinks_packets_received += sink.n_packets_received
        total_sinks_packets_lost += sink.n_packets_not_received
        #print(str(sink) + "received " + str(sink.n_packets_received))
        #print(str(sink) + "not received " + str(sink.n_packets_not_received))


    node_avg_speed = round(summation_nodes_speed/len(nodes),2)
    print("Average speed of nodes : "+ str(round(summation_nodes_speed/len(nodes),2))+ "km/h")  
    avg_node_gen_packet = round(summation_nodes_gen_rates/len(nodes),2)
    print("Average packets generation rate of nodes : "+ str(round(summation_nodes_gen_rates/len(nodes),2))+ " per step")  
    print("Total number of packets generated by nodes : "+str(total_nodes_packets_generated))
    print("Total number of packets transferred by nodes to other nodes : "+str(total_nodes_packets_transferred))
    print("Total number of packets lost by nodes : "+str(total_nodes_packets_lost))
    print("Total number of packets received by sinks : "+str(total_sinks_packets_received))
    print("Total number of packets lost by sinks : "+str(total_sinks_packets_lost))

    fig = plt.figure(figsize=(18,9))
    axs = fig.subplots(2, 2)
    fig.suptitle('Network traffic per time unit\n' + 'Simulation ' + str(n_sim) + ' - Number of nodes: ' + str(len(nodes)) + ' - Number of Sinks: ' + str(len(sinks)) + '\nThe following nodes stopped working during the simulation: ' + str(will_crash))

    axs[0,0].plot(range(1,61), traffic_nodes, 'o-', color='green')
    axs[0,0].plot(range(1,61), lost_traffic_nodes, 'o-', color='red')
    axs[0,0].set_title('Packets exchanged between nodes per unit of time (green)\nagainst packets whose exchange failed (red)')
    axs[0,1].plot(range(1,61), traffic_sinks, 'o-', color='green')
    axs[0,1].plot(range(1,61), lost_traffic_sinks, 'o-', color='red')
    axs[0,1].set_title('Packets exchanged between nodes and sinks per unit of time (green)\nagainst packets whose exchange failed (red)')
    axs[1,0].bar(range(1,61), pkts_generated_per_t)
    axs[1,0].set_title('Packets generated by all active nodes per time unit')
    print(sinks_fullness)
    rot_sinks_fullness = [[x[i] for x in sinks_fullness] for i in range(len(sinks_fullness[0]))]
    colors = ['mediumvioletred', 'midnightblue', 'orange', 'royalblue', 'tomato', 'forestgreen', 'maroon', 'limegreen', 'dimgray', 'slateblue']
    for i in range(len(sinks)):
        axs[1,1].plot(range(1,61), rot_sinks_fullness[i], 'o-', color=colors[i])
    axs[1,1].set_title('Amount of memory occupied by received packets in each sink')
    plt.show()

    return len(nodes), len(sinks), node_avg_speed, avg_node_gen_packet, total_nodes_packets_generated, total_nodes_packets_transferred, total_nodes_packets_lost, total_sinks_packets_received, total_sinks_packets_lost
    




def main():

    n_nodes = []
    n_sinks = []
    node_avg_speed = []
    avg_node_gen_packet = []
    total_nodes_packets_generated = []
    total_nodes_packets_transferred = []
    total_nodes_packets_lost = []
    total_sinks_packets_received = []
    total_sinks_packets_lost = []
    sim_num = range(10)

    simulation_map, sinks, nodes = prepare_map()    # so we can maintain the same conditions among more simulations 

    sim_groups = 1

    for sim in range(sim_groups*3):

        if(sim%3==0 and sim!=0):
            simulation_map, sinks, nodes = prepare_map()

        # if we maintain the same nodes and sinks, we need to "clean" them up
        for node in nodes:
            node.n_packets_generated = 0
            node.n_packets_received = 0
            node.n_packets_not_received = 0
            node.n_packets_sent = 0
            node.n_packets_not_sent = 0
            node.set_active(ac=True)
            node.packets_generated.queue.clear()
            node.packets_received.queue.clear()
            node.set_position(coords=node.get_start())
        for sink in sinks:
            sink.n_packets_received = 0
            sink.n_packets_not_received = 0
            sink.packets_received.queue.clear()
            sink.set_active(ac=True)

        if sim%3==1:
            n_n, n_s, nas, angp, tnpg, tnpt, tnpl, tspr, tspl = execute_simulation(sim_map=simulation_map, param_sinks=sinks, param_nodes=nodes, crash_nodes=3, n_sim=sim+1)
        elif sim%3==2:
            n_n, n_s, nas, angp, tnpg, tnpt, tnpl, tspr, tspl = execute_simulation(sim_map=simulation_map, param_sinks=sinks, param_nodes=nodes, crash_nodes=5, n_sim=sim+1)
        else:
            n_n, n_s, nas, angp, tnpg, tnpt, tnpl, tspr, tspl = execute_simulation(sim_map=simulation_map, param_sinks=sinks, param_nodes=nodes)
        if(tnpt != 0 or tspr != 0 or tnpl!=0 or tspl!=0):
            n_nodes.append(n_n)
            n_sinks.append(n_s)
            node_avg_speed.append(nas)
            avg_node_gen_packet.append(angp)
            total_nodes_packets_generated.append(tnpg)
            total_nodes_packets_transferred.append(tnpt)
            total_nodes_packets_lost.append(tnpl)
            total_sinks_packets_received.append(tspr)
            total_sinks_packets_lost.append(tspl)

    print("\n\n")
    for i in range(len(n_nodes)):
        print("Simulazione " + str(i) + ") Nodi: " + str(n_nodes[i]) + ", Sinks: " + str(n_sinks[i]))
        print("Average speed of nodes : "+ str(node_avg_speed[i])+ "km/h")  
        print("Average packets generation rate of nodes : "+ str(avg_node_gen_packet[i])+ " per step")  
        print("Total number of packets generated by nodes : "+str(total_nodes_packets_generated[i]))
        print("Total number of packets transferred by nodes to other nodes : "+ str(total_nodes_packets_transferred[i]))
        print("Total number of packets lost by nodes : "+ str(total_nodes_packets_lost[i]))
        print("Total number of packets received by sinks : "+ str(total_sinks_packets_received[i]))
        print("Total number of packets lost by sinks : "+str(total_sinks_packets_lost[i]))

    sim_num = range(len(n_nodes))
    fig = plt.figure(figsize=(17,10))
    axs = fig.subplots(2, 2)
    fig.suptitle('Total data from ' + str(sim_groups*3) + ' simulations')
    axs[0, 0].scatter(sim_num, avg_node_gen_packet, marker='o')
    axs[0, 0].set_title('Average pkts generation rate of nodes')
    axs[0, 1].scatter(sim_num, total_nodes_packets_transferred, marker='o', c='green')
    axs[0, 1].scatter(sim_num, total_nodes_packets_lost, marker='o', c='red')
    axs[0, 1].set_title('Total number of pkts exchanged between nodes (green) and lost ones (red)')
    axs[1, 0].scatter(sim_num, total_sinks_packets_received, marker='o', c='green')
    axs[1, 0].scatter(sim_num, total_sinks_packets_lost, marker='o', c='red')
    axs[1, 0].set_title('Total number of pkts exchanged with sinks (green) and lost ones (red)')
    plt.show()
    # axs[1, 1].plot(x, -y, 'tab:red')
    # axs[1, 1].set_title('Axis [1, 1]')
    
    '''
    #plt.scatter(sim_num, node_avg_speed, marker='x')
    plt.scatter(sim_num, avg_node_gen_packet, marker='o')
    #plt.scatter(sim_num, total_nodes_packets_generated, marker='o', c='black')
    plt.scatter(sim_num, total_nodes_packets_transferred, marker='o', c='red')
    plt.scatter(sim_num, total_nodes_packets_lost, marker='o', c='brown')
    plt.scatter(sim_num, total_sinks_packets_received, marker='o', c='green')
    plt.scatter(sim_num, total_sinks_packets_lost, marker='o', c='yellow')
    plt.show()
    '''


if __name__ == "__main__":
    main()