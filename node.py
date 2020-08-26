from waypoint import Waypoint

class Node:

    def __init__(self, coords=[-1,-1], start=[-1,-1], target=[-1,-1]):
        self.position = Waypoint(coordinates=coords)
        self.start = Waypoint(coordinates=start)
        self.target = Waypoint(coordinates=target)

    def set_position(self, coords):
        self.position.set_coordinates(coords)
        return None

    def get_position(self):
        return self.position.get_coordinates()

    def set_start(self, coords):
        self.start.set_coordinates(coords)
        return None

    def get_start(self):
        return self.start.get_coordinates()

    def set_target(self, coords):
        self.target.set_coordinates(coords)
        return None

    def get_target(self):
        return self.target.get_coordinates()