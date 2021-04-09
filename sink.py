from waypoint import Waypoint
import queue
from node import Node

class Sink:
    
    def __init__(self, id=99, coords=[-1,-1], active=True):
        self.id = id
        self.position = Waypoint(coordinates=coords)
        self.n_packets_received = 0
        self.n_packets_not_received = 0
        self.packets_received = queue.Queue(350)
        self.active = active
        
    
    def get_id(self):
        return self.id
    
    def set_id(self, i):
        self.id = i
        return None
    
    def set_active(self, ac):
        self.active = ac
        return None

    def get_active(self):
        return self.active


    def get_position(self):
        return self.position.get_coordinates()
    
    def message_received(self, message):
        self.queue.add(message)
        
    def message_exchange(self, node):
        print(f"Sink in position {self.get_position()} is trying to exchange packets with node {node.get_id()}")
        speed_node = node.get_speed()
        transmission = node.get_transmission_time()
        signal_intensity = speed_node * transmission
        print(f"The signal intensity is: {signal_intensity}")
        if signal_intensity < 60:
            print("The exchange between sink and node is taking place")
            # The sink gathers both the packets generated by the node and the packets that the node received from other nodes
            # If the sinks memory becomes full, packets are lost
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