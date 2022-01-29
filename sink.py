from waypoint import Waypoint
from queue import Queue
from node import Node

class Sink:
    
    def __init__(self, id=0, coordinates=[-1,-1], status=True, memory=100, log=True):
        self.id = id
        self.position = Waypoint(coordinates=coordinates)
        self.n_packets_received = 0
        self.n_packets_not_received = 0
        self.status = status
        self.memory = Queue(memory)
        self.log = True
        # Keep track of succeeded/failed transmissions
        self.good_exchanges = 0
        self.bad_exchanges = 0
    
    def get_id(self):
        return self.id
    
    def set_id(self, i):
        self.id = i
        return None
    
    def set_status(self, status):
        self.status = status 
        return None

    def get_status(self):
        return self.active

    def get_position(self):
        return self.position.get_coordinates()
    
    def receive_message(self, message):
        self.memory.add(message)
        
    def get_exchange_stat(self):
        total_exchanges = self.good_exchanges + self.bad_exchanges
        return bad_exchanges, good_exchanges, total_exchanges
        
    def exchange_message(self, node):
        print(f"Sink in position {self.get_position()} is trying to exchange packets with node {node.get_id()}")
        speed_node = node.get_speed()
        transmission = node.get_transmission_time()
        # TODO: use a metric to establish a uniform signal intensity
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