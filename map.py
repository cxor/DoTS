from waypoint import Waypoint
import numpy as np


class Map:

    # WAYPOINT_ACTIVATION_STOC_V = [0.95, 0.50, 0.25, 0.15]
    WAYPOINT_ACTIVATION_STOC_V = [0.95, 0.60, 0.45, 0.25]
    # WAYPOINT_ACTIVATION_STOC_V = [0.8]

    # Map object is defined by:
    #   - topology [blank, roads]
    #   - boundaries
    #   - structure [None, WaypointNetwork]
    # ------------------------------------------------------------------
    # "structure" instance field is decoupled from "topology" instance field
    # because it can express different features for the same topology (i.e.
    # WaypointNetwork with physical obstacles, ...)

    def __init__(self, topology="blank", size=[100, 100]):
        self.topology = topology
        self.size = size
        self.active_locations = []
        self.initialize_map(topology=self.topology, size=self.size)

    def get_topology(self):
        return self.topology

    def draw_topology(self):
        if self.topology is not None:
            for col in range(self.size[1]):
                for row in range(self.size[0]):
                    if self.topology[col][row].get_status() == 1:
                        # print("\u25cf", sep=" ", end="")
                        print("\u2022", sep=" ", end="")    # road
                    else:
                        # print("\u25cb", sep=" ", end="")
                        print("\u0394", sep=" ", end="")    # obstacle
                    if row == (self.size[0] - 1):
                        print()
        return None

    def get_size(self):
        return self.size

    def get_active_locations(self):
        return self.active_locations

    def initialize_map(self, topology, size):
        if topology == "blank":
            self.topology = None
            self.active_locations = None
        else:
            # topology is road-based     
            self.topology = self.generate_waypoint_network(size)
            for i in range(self.size[1]):
                for j in range(self.size[0]):
                    if self.topology[i][j].get_status() == 1:
                        self.active_locations.append(self.topology[i][j])
        return None

    def generate_waypoint_network(self, size):
        columns_no = size[0]
        rows_no = size[1]
        waypoint_matrix = np.full(shape=(rows_no,columns_no), fill_value=Waypoint())
        for i in range(rows_no):
            for j in range(columns_no):
                waypoint_matrix[i][j] = Waypoint(coordinates=[i,j])
        map_entry_point = waypoint_matrix[0][0]
        map_entry_point.set_status(1)
        map_entry_point.set_coordinates([0,0])
        initial_row = True
        for i in range(rows_no):
            end_row = False   
            for j in range(columns_no):
                end_column = False
                current_waypoint = waypoint_matrix[i][j]
                if not current_waypoint.get_status() == 1:
                    continue

                if (i == 0) and (j != columns_no-1):
                    ################# print("FIRST_ROW, not LAST_COL")
                    # Whenever (j == columns_no) applies, the relative
                    # section below is used to select eligible neighbors,
                    # restricting the overall possibilies for the current
                    # border waypoint.
                    # print("\nHERE 1")
                    eligible_neighbors = [waypoint_matrix[i][j+1],
                                            waypoint_matrix[i+1][j],
                                            waypoint_matrix[i+1][j+1]]
                    initial_row = True

                if (i == rows_no-1) and (j != columns_no-1):
                    # print("\nHERE 2")
                    ### Last row of the waypoint matrix
                    eligible_neighbors = [waypoint_matrix[i][j+1],
                                            waypoint_matrix[i-1][j+1]]
                    end_row = True

                if (j == columns_no-1):
                    # print("\nHERE 3")
                    # Last column of the waypoint matrix
                    end_column = True
                    initial_row = False
                    if (i != rows_no-1):
                        eligible_neighbors = [waypoint_matrix[i+1][j]]

                if end_column and end_row:
                    return waypoint_matrix
                
                if (i != 0) and (i != rows_no-1) and (j != columns_no-1):
                    ### Common case: Chebyshev 8-way connections
                    # print("\nHERE")
                    eligible_neighbors = [waypoint_matrix[i-1][j+1],
                        waypoint_matrix[i][j+1],
                        waypoint_matrix[i+1][j],
                        waypoint_matrix[i+1][j+1]]
                
                # print("Waypoint:"+str(current_waypoint.get_coordinates())+" Eligible neighbors:")
                # for neighbor_waypoint in eligible_neighbors:
                #     print(str(neighbor_waypoint.get_coordinates()))

                for neighbor_waypoint in eligible_neighbors:
                    activation_seed = round(np.random.uniform(0, 1), 2)
                    activation_threshold = np.random.choice(Map.WAYPOINT_ACTIVATION_STOC_V)
                    # print(f"Waypoint: {current_waypoint.get_coordinates()} - {activation_seed},{activation_threshold} ", end="")
                    if activation_seed <= activation_threshold:
                        current_waypoint.add_neighbor(neighbor_waypoint)
                        neighbor_waypoint.add_neighbor(current_waypoint)
                        neighbor_waypoint.set_status(1)
                        # print(" OK ->" + str(neighbor_waypoint.get_coordinates()))
                    else:
                        pass
                        ### print("NOPE")
        return waypoint_matrix