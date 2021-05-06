class Waypoint:
    
    LOG = True
    
    def __init__(self, coordinates=[-1,-1], neighbors=[], status=0, entity="empty"):
        self.coordinates = coordinates
        self.neighbors = neighbors
        self.status = status    
        # Waypoint status legend:
        #   0 -> inactive waypoint
        #   1 -> active waypoint
        #   2 -> disastered waypoint
        self.entity = entity
        # Waypoint entity legend:
        #   "empty" -> no network entity is present on the waypoint
        #   "node" -> a node is present on the waypoint
        #   "sink" -> a sink is present on the waypoint
        #   "obstacle" -> an obstacle is present on the waypoint

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status
    
    def set_entity(self, entity):
        self.entity = entity

    def get_entity(self):
        return self.entity

    def log(self):
        if Waypoint.LOG == True:
            print(f"Waypoint coordinates: {self.coordinates}, \
                status: {self.status}, entity: {self.entity}")
    
    