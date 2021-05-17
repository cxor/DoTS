from waypoint import Waypoint
from queue import PriorityQueue

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
        exploration_heap = PriorityQueue()
        current_waypoint = self.start
        closed_frontier = []
        route = []
        
        exploration_heap.push(self.start, self.get_trajectory_cost(self.start))
        route.append(self.start.get_coordinates())
        while not exploration_heap.empty():
            current_waypoint = exploration_heap.pop()
            if current_waypoint == self.target:
                return route
            closed_frontier.add(current_waypoint)
            for neighbor in current_waypoint.get_neighbors():
                if neighbor not in closed_frontier:
                    trajectory_cost = self.get_trajectory_cost(neighbor)
                    exploration_heap.push(neighbor, trajectory_cost)
                else:
                    continue
        return None
    

    def get_trajectory_cost(self, waypoint):
        route_cost = 0 # g
        estimate_cost = 0 # h
        trajectory_cost = 0 # f
        route_cost = abs(waypoint.get_coordinates()[0] - self.start.get_coordinates[0]) \
                     + abs(waypoint.get_coordinates()[1] - self.start.get_coordinates()[1])
        estimate_cost = abs(waypoint.get_coordinates()[0] - self.target.get_coordinates[0]) \
                     + abs(waypoint.get_coordinates()[1] - self.target.get_coordinates()[1])
        
        trajectory_cost = route_cost + estimate_cost
        return trajectory_cost


    def get_position(self):
        return self.position

    def get_route(self):
        return self.route
    