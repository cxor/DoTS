class Waypoint:

    def __init__(self, coordinates=[-1,-1], neighbors=[], status=0):
        self.coordinates = coordinates
        self.neighbors = neighbors
        self.status = status    # 0: obstacle, 1: road (empty), 2: node (on the road)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
        return None

    def get_coordinates(self):
        return self.coordinates

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        return None

    def set_status(self, status):
        self.status = status
        return None

    def get_status(self):
        return self.status

    def show_info(self):
        print(f"Waypoint coordinates: {self.coordinates}, status: {self.status}")
        return None