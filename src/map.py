from waypoint import Waypoint
from node import Node
from sink import Sink
from navigator import Navigator
import numpy
import random

class Map:

    WAYPOINT_ACTIVATIONS = [0.95, 0.60, 0.45, 0.25]
    LOG = True

    def __init__(self, size=[100,100]):
        self.size = size
        self.nodes = []
        self.sinks = []
        self.network = []
        
    def get_network(self):
        return self.network

    def get_size(self):
        return self.size

    def get_nodes(self):
        return self.nodes

    def get_sinks(self):
        return self.sinks

    def build(self, no_nodes, no_sinks, node_signal, sink_signal,
              node_speed, fault, transmission_rate):
        # Create a map inline with desired specifications
        no_available_positions = 0
        while no_available_positions < (no_nodes + no_sinks):
            self.network = self.generate_network(self.size)
            no_available_positions = len(self.get_available_positions())
        self.add_sinks(no_sinks, sink_signal, fault)
        self.add_nodes(no_nodes, node_signal, 
                       node_speed, fault, transmission_rate)

    def generate_network(self, size):
        # The following method designs a waypoint network for the map.
        # It can be decomposed in 2 main stages:
        #   1. Create the waypoint skeleton
        #   2. Then, for every waypoint:
        #       2.1 Build a list of neighbors eligible for activation
        #       2.2 Randomly activate some of its eligible neighbors
        # -------------------------------------        
        # Stage 1: create the waypoint skeleton
        rows_no, columns_no = size[0], size[1]
        waypoint_matrix = numpy.full(shape=(rows_no,columns_no), fill_value=Waypoint())
        for i in range(rows_no):
            for j in range(columns_no):
                waypoint_matrix[i][j] = Waypoint(coordinates=[i,j])
        # -------------------------------------        
        # Stage 2.1: build a list of neighbors eligible for activation
        map_entry_point = waypoint_matrix[0][0]        
        map_entry_point.set_status(1)
        for i in range(rows_no):
            for j in range(columns_no):
                current_waypoint = waypoint_matrix[i][j]
                if not current_waypoint.get_status() == 1:
                    continue
                # Common case: current waypoint is not on borders
                if (i != 0) and (i != rows_no-1) and (j != columns_no-1):
                    eligible_neighbors = [waypoint_matrix[i-1][j+1],
                                            waypoint_matrix[i][j+1],
                                            waypoint_matrix[i+1][j],
                                            waypoint_matrix[i+1][j+1]]
                # Corner case: first row, but not last column 
                if (i == 0) and (j != columns_no-1):
                    eligible_neighbors = [waypoint_matrix[i][j+1],
                                            waypoint_matrix[i+1][j],
                                            waypoint_matrix[i+1][j+1]]
                # Corner case: last rows, but not last column
                if (i == rows_no-1) and (j != columns_no-1):
                    eligible_neighbors = [waypoint_matrix[i][j+1],
                                            waypoint_matrix[i-1][j+1]]
                # Corner case: last column + exit point
                if (j == columns_no-1):
                    if (i != rows_no-1):
                        eligible_neighbors = [waypoint_matrix[i+1][j]]
                    else:
                        return waypoint_matrix
                # -------------------------------------        
                # Stage 2.2: randomly activate some of the waypoint eligible neighbors
                for neighbor_waypoint in eligible_neighbors:
                    activation_seed = round(numpy.random.uniform(0,1), 2)
                    activation_threshold = numpy.random.choice(Map.WAYPOINT_ACTIVATIONS)
                    if activation_seed <= activation_threshold:
                        current_waypoint.add_neighbor(neighbor_waypoint)
                        neighbor_waypoint.add_neighbor(current_waypoint)
                        neighbor_waypoint.set_status(1)
        return waypoint_matrix
    
    def add_sinks(self, no_sinks, sink_signal, sink_fault):
        available_positions = self.get_available_positions()
        sink_locations = random.sample(available_positions, no_sinks)
        for i in range(no_sinks):
            current_waypoint = sink_locations[i]
            sink = Sink(id=i, coordinates=current_waypoint.get_coordinates(), \
                signal=sink_signal, fault=sink_fault)
            self.sinks.append(sink)
            # TODO: remove entity?
            current_waypoint.set_entity("sink") 

    def add_nodes(self, no_nodes, node_signal, node_speed, 
                  node_fault, transmission_rate):
        available_positions = self.get_available_positions()
        node_locations = random.sample(available_positions, no_nodes)
        node_targets = random.sample(available_positions, no_nodes)
        for i in range(no_nodes):
            start_waypoint = node_locations[i]
            target_waypoint = node_targets[i]
            navigator = Navigator(start=start_waypoint, \
                target=target_waypoint, network=self.network)
            node = Node(id=i, signal=node_signal, speed=node_speed, \
                    navigator=navigator, fault=node_fault, \
                    transmission_rate=transmission_rate)
            self.nodes.append(node)
            # TODO: remove entity?
            start_waypoint.set_entity("node")

    def get_available_positions(self):
        rows_no, columns_no = self.size[0], self.size[1]
        available_positions = []
        for i in range(rows_no):
            for j in range(columns_no):
                current_waypoint = self.network[i][j]
                if current_waypoint.get_status() == 1 \
                    and current_waypoint.get_entity() == "empty":
                    available_positions.append(current_waypoint)
        return available_positions

    def update(self, disaster):
        # TODO: implement here the code to trigger node movement, 
        # message exchange, random fault and random disasters
        if disaster:
            # 1. randomically select an area to apply the disaster into
            # 2. set the status of every entity in the area above to 0
            # 3.

            pass
        else:
            pass 
        

    def print(self):
        if Map.LOG == True:
            rows_no, columns_no = self.size[0], self.size[1]
            for i in range (rows_no):
                for j in range (columns_no):
                    current_waypoint = self.network[i][j]
                    if (j != columns_no-1):
                        carriage = ""
                    else:
                        carriage = "\n"
                    print(current_waypoint.get_status(),end=carriage)
