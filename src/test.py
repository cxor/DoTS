from node import Node
from sink import Sink
from simulator import Simulator
from map import Map
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def create_simulator():
    no_nodes = 10
    no_sinks = 5
    node_signal = 15
    sink_signal = 20
    node_speed = 10
    transmission_rate = 10
    fault = 0.1
    disaster = 3
    map_size = [50, 50]
    simulation_seconds = 20
    simulator = Simulator(           \
            no_nodes=no_nodes,       \
            no_sinks=no_sinks,       \
            node_signal=node_signal, \
            sink_signal=sink_signal, \
            node_speed=node_speed,   \
            fault=fault,             \
            disaster=disaster,       \
            map_size=map_size,       \
            transmission_rate=transmission_rate, \
            duration=simulation_seconds)
    print(simulator.get_entities_params())
    return simulator

def populate_map():
    simulator = create_simulator()
    simulator.populate()
    for node in simulator.get_nodes():
        print("Active node: " + node.get_id())
    for sink in simulator.get_sinks():
        print("Active sink: " + sink.get_id())

def launch_batch_simulations():
    no_batch_simulations = 3
    no_nodes = [50, 100, 200]
    no_sinks = [25, 50, 100]
    node_signal = [15, 12, 10]
    sink_signal = [20, 17, 15]
    node_speed = [12, 24, 36]
    transmission_rate = [10, 20, 50]
    fault = [0.1, 0.3, 0.4]
    disaster = [0, 0.1, 0.2]
    map_size = [40, 40]
    simulation_seconds = 20 

    stats = numpy.array([.0,.0,.0,.0,.0])
    stats_per_epoch = []
    # -----------------------------------
    for i in range(no_batch_simulations):
        simulator = Simulator(          \
            no_nodes=no_nodes[i],       \
            no_sinks=no_sinks[i],       \
            node_signal=node_signal[i], \
            sink_signal=sink_signal[i], \
            node_speed=node_speed[i],   \
            fault=fault[i],             \
            disaster=disaster[i],       \
            map_size=map_size,          \
            transmission_rate=transmission_rate[i], \
            duration=simulation_seconds)
        simulator.run()
        stats += simulator.get_stats()
        stats_per_epoch.append(simulator.get_stats())
        #simulator.plot() 
    stats /= no_batch_simulations
    plot(stats, stats_per_epoch)   
                
def message_exchange():
    simulator = create_simulator()
    simulator.populate()
    nodes = simulator.get_nodes()
    sinks = simulator.get_sinks()
    node_1 = nodes[0]
    node_2 = nodes[1]
    sink_1 = sinks[0]
    node_1.send_message(receiver=sink_1, message_type="info")
    node_2.send_message(receiver=node_1, message_type="sos")
    print(f"Node 1 buffer count: {node_1.get_buffer().qsize()}")
    print(f"Node 2 buffer count: {node_2.get_buffer().qsize()}")


def print_map():
    map = Map(size=[5,5])
    map.print()
    
def print_neighbors():
    map = Map(no_nodes=10, no_sinks=10, node_signal=10,
              sink_signal=15, node_speed=10, fault=0, 
              transmission_rate=1, size=[50,50])
    waypoint_matrix = map.get_network()

def find_route():
    simulator = create_simulator()
    simulator.populate()
    nodes = simulator.get_nodes()
    for node in nodes:
        navigator = node.get_navigator()
        print(f"Node {node.get_id()} route: {navigator.get_route()}")

def plot(stats, stats_per_epoch):


    fig, axs = plt.subplots(2)
    
    msg = ['Info', 'SOS']
    epoch = range(len(stats_per_epoch))

    width = 0.1

    axs[0].bar(msg[0], stats[2], width, color='r')
    axs[0].bar(msg[0], stats[0], width, bottom=stats[2], color='b')
    axs[0].bar(msg[1], stats[3], width, color='r')
    axs[0].bar(msg[1], stats[1], width, bottom=stats[3], color='b')
    
    axs[0].legend(labels=['Dropped', 'Received'])

    for i in epoch:

        axs[1].scatter(i, stats_per_epoch[i][0], marker='-o', color='r', linestyle='solid')
        axs[1].scatter(i, stats_per_epoch[i][1], marker='-o', color='b', linestyle='solid')
        axs[1].scatter(i, stats_per_epoch[i][2], marker='-o', color='y', linestyle='solid')
        axs[1].scatter(i, stats_per_epoch[i][3], marker='-o', color='g', linestyle='solid')
        axs[1].scatter(i, stats_per_epoch[i][4], marker='-o', color='o', linestyle='solid')

    axs[1].xlabel('Epochs')
    axs[1].ylabel('Average')
    axs[1].legend(labels=['Average info message received', 
                          'Average sos message received',
                          'Average info message dropped',
                          'Average sos message dropped',
                          'Average fault rate'])
    
    plt.show()


if __name__ == "__main__":
    launch_batch_simulations()