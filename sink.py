from waypoint import Waypoint
import queue


class Sink:
    
    def __init__(self, coords=[-1,-1]):
        self.position = Waypoint(coordinates=coords)
        self.queue = queue.Queue()
        
    def get_position(self):
        return self.position.get_coordinates()
    
    def message_received(self, message):
        self.queue.add(message)