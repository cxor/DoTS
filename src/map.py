from waypoint import Waypoint
from node import Node
from sink import Sink
from navigator import Navigator
import numpy
import random

class Map:

    WAYPOINT_ACTIVATIONS = [0.95, 0.60, 0.45, 0.25]
    LOG = True

    def __init__(self, size=[100,100], no_active_locations=2):                    
        self.size = size
        self.no_active_locations = no_active_locations
        self.network = []
        ### self.nodes, self.sinks, self.network = [], [], []
        no_available_positions = 0
        while no_available_positions < (no_active_locations):
            self.network = self.generate_network()
            no_available_positions = len(self.get_available_positions())
        
    def get_network(self):
        return self.network

    def get_size(self):
        return self.size

    def generate_network(self):
        size = self.size
        # The following method designs a waypoint network for the map.
        # It can be decomposed in 2 main stages:
        #   1. Create the waypoint skeleton
        #   2. Then, for every waypoint:
        #       2.1 Build a list of neighbors eligible for activation
        #       2.2 Randomly activate some of its eligible neighbors
        # -------------------------------------        
        # Stage 1: create the waypoint skeleton
        rows_no, columns_no = int(size[0]), int(size[1])
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

    def get_available_positions(self):
        rows_no, columns_no = int(self.size[0]), int(self.size[1])
        available_positions = []
        for i in range(rows_no):
            for j in range(columns_no):
                current_waypoint = self.network[i][j]
                if current_waypoint.get_status() == 1 \
                    and current_waypoint.get_entity() == "empty":
                    available_positions.append(current_waypoint)
        return available_positions

    def update(self, disaster):
        for node in self.nodes:
            if disaster:
                if not node.simulate_fault(disaster):
                    # the node does not move along
                    for receiver in self.nodes:
                        node.send_message(receiver, "sos")
                    for receiver in self.sinks:
                        node.send_message(receiver, "sos")
            elif node.simulate_fault():
                node.move()    
            else:
                node.move()
                for receiver in self.nodes:
                    node.send_message(receiver, "info")
                for receiver in self.sinks:
                    node.send_message(receiver, "info")

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
