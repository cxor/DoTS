from waypoint import Waypoint

class Navigator:

    def __init__(self, start=[0,0], target=[0,0], network=None):
        self.position = start
        self.start = start
        self.target = target
        # The network attribute is just the waypoint matrix of the map
        self.network = network
        self.route = self.find_route()


    def find_route(self):
        """
        The following method implement the A*-pathfinding
        algorithm. In order to reach the target from a
        starting position, the navigator will go through
        3 main steps:
            1. Generate a list of possible states towards the
            target from the current position
            2. Store in a priority queue such states based on
            distance to target, the closest goes first
            3. Select closest state and repeat until the target
            is reached or there are no more states
        """
        route_cost = 0 # g
        estimate_cost = 0 # h
        
        if self.position == self.target:
            route = []
            while self.position != self.start:
                route.append(self.position)
    
    def get_position(self):
        return self.position
    