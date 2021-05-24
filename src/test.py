from node import Node
from sink import Sink
from map import Map


def message_exchange():
    map = Map(no_nodes=10, no_sinks=10, node_signal=10,
          sink_signal=15, node_speed=10, fault=0, 
          transmission_rate=1, size=[50,50])
    nodes = map.get_nodes()
    sinks = map.get_sinks()
    node_1 = nodes[0]
    node_2 = nodes[1]
    sink_1 = sinks[0]
    sink_2 = sinks[1]
    node_1.send_message(receiver=sink_1, message_type="info")
    node_2.send_message(receiver=node_1, message_type="sos")
    print(f"Node 1 buffer: {node_1.get_buffer()}")
    print(f"Node 2 buffer: {node_2.get_buffer()}")


def print_map():
    map = Map(size=[5,5])
    map.print()
    
def print_neighbors():
    map = Map(no_nodes=10, no_sinks=10, node_signal=10,
              sink_signal=15, node_speed=10, fault=0, 
              transmission_rate=1, size=[50,50])
    waypoint_matrix = map.get_network()

def find_route():
    map = Map(no_nodes=10, no_sinks=10, node_signal=10,
              sink_signal=15, node_speed=10, fault=0, 
              transmission_rate=1, size=[50,50])
    map.print()
    nodes = map.get_nodes()
    for node in nodes:
        navigator = node.get_navigator()
        print(f"Node {node.get_id()} route: {navigator.get_route()}")
    
    
        # Insert the starting waypoint coordinates into the route