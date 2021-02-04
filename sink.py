from waypoint import Waypoint


class Sink:
    
    def __init__(self, coords=[-1,-1]):
        self.position = Waypoint(coordinates=coords)
        
    def get_position(self):
        return self.position.get_coordinates()