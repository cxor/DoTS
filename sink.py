from waypoint import Waypoint
import queue
from node import Node

class Sink:
    
    def __init__(self, coords=[-1,-1]):
        self.position = Waypoint(coordinates=coords)
        self.n_packets_received = 0
        self.n_packets_not_received = 0
        self.packets_received = queue.Queue(100)
        
    def get_position(self):
        return self.position.get_coordinates()
    
    def message_received(self, message):
        self.queue.add(message)
        
    def message_exchange(self, node):
        speed_node = node.get_speed()
        transmission = node.get_transmission_time()
        signal_intensity = speed_node * transmission
        print(signal_intensity)
        if signal_intensity < 60:
            print("Messages exchanged with sink")
            while node.packets_generated.qsize()!=0:
                if not (self.packets_received.full()):
                    self.packets_received.put(node.packets_generated.get())
                    self.n_packets_received += 1
                else:
                    node.packets_generated.get()
                    self.n_packets_not_received +=1
            
            while node.packets_received.qsize()!=0:
                if not (self.packets_received.full()):
                    self.packets_received.put(node.packets_received.get())
                    self.n_packets_received += 1
                else:
                    node.packets_received.get()
                    self.n_packets_not_received +=1