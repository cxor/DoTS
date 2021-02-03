from waypoint import Waypoint

class Node:

    def __init__(self, transmission_time=0, speed=0, coords=[-1,-1], start=[-1,-1], target=[-1,-1], par=None):
        self.position = Waypoint(coordinates=coords)
        self.start = Waypoint(coordinates=start)
        self.target = Waypoint(coordinates=target)
        self.path = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = par
        self.transmission_time = transmission_time
        self.speed = speed
        self.packet_received = 0
        self.packet_not_received = 0
        
    def get_transmission_time(self):
        return self.transmission_time
    
    def get_speed(self):
        return self.speed
        
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

    def set_parent(self,p):
        self.parent = p
        return None

    def get_parent(self):
        return self.parent
    
    def get_received_packet(self):
        return self.packet_received
    
    def get_not_received_packet(self):
        return self.packet_not_received

    def set_path(self, network_matrix):
        core_path = self.movement(topology=network_matrix)
        self.path = []
        (self.path).append(self.get_start())
        for i in core_path:
            (self.path).append(i)
        for i in reversed(core_path):   # this because we need to go back and forth
            (self.path).append(i)
        return None

    def get_path(self):
        return self.path

    def movement(self, topology):
        # Here I want to determine the path that the node will follow
        # The end result is that the node keeps on going back and forth from start to target (and viceversa)
        # for the entire simulation
        # It uses a kind of A*-like algorithm to determine the waypoints it will touch

        open = []
        closed = []

        start_node = Node(coords=self.get_start())
        goal_node = Node(coords=self.get_target())

        open.append(start_node)

        while len(open)>0:

            current_node = open.pop(0)

            closed.append(current_node)

            if current_node.get_position() == goal_node.get_position():
                path = []
                while current_node.get_position() != start_node.get_position():
                    path.append(current_node.get_position())
                    current_node = current_node.get_parent()
                return path[::-1]

            (x,y) = current_node.get_position()

            neighbors = [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1]]
            # neighbors = [[x-1,y],[x,y+1],[x+1,y],[x,y-1]]     # WITHOUT DIAGONALS

            for next in neighbors:

                if(next[0]>9):
                    continue
                if(next[1]>19):
                    continue
                if(next[0]<0):
                    continue
                if(next[1]<0):
                    continue

                map_value = topology.topology[next[0]][next[1]].get_status()
 
                if(map_value == 0):
                    continue

                neighbor = Node(coords=[next[0],next[1]], par=current_node)

                if (neighbor in closed):
                    continue

                neighbor.g = abs(neighbor.get_position()[0] - start_node.get_position()[0]) + abs(neighbor.get_position()[1] - start_node.get_position()[1])
                neighbor.h = abs(neighbor.get_position()[0] - goal_node.get_position()[0]) + abs(neighbor.get_position()[1] - goal_node.get_position()[1])
                neighbor.f = neighbor.g + neighbor.h

                if(add_to_open(open,neighbor) == True):
                    # print("start: " + str(start_node.get_position()) + " target: " + str(goal_node.get_position()))
                    open.append(neighbor)

        return None     # no path is found - should not happen
    
    def exchange_message(self, node):
        
        #check the probability of exchange messages
        speed_node1 = node.get_speed()
        transmission1 = node.get_transmission_time()
        speed_node2 = self.get_speed()
        transmission2 = self.get_transmission_time()
        signal_intensity = abs(speed_node1 + speed_node2)*(transmission1 + transmission2)
      
        if signal_intensity > 3:
            print("bomba")
            self.packet_received += 1
            print(self.packet_received)
        else:
            self.packet_not_received += 1
    

def add_to_open(open, neighbor):
    for node in open:
        if (neighbor.get_position() == node.get_position() and neighbor.f >= node.f):
            return False
    return True