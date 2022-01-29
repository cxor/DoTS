from waypoint import Waypoint
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class ComparableWaypoint:
    priority: int
    waypoint: Any=field(compare=False)
class Navigator:

    LOG = True
    
    def __init__(self, start=[0,0], target=[0,0], network=None):
        self.position = 0
        self.start = start
        self.target = target
        # The network attribute is just the waypoint matrix of the map
        self.network = network
        self.route = self.find_route()
        self.full_route = self.route + self.route[-1:1]

    def find_route(self):
        """
        The following method implements the A*-pathfinding
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
        closed_frontier, route, parents = [], [], {}
        
        comparable_waypoint = \
            ComparableWaypoint(self.get_trajectory_cost(self.start), self.start)
        exploration_heap.put(comparable_waypoint)
        route.append(self.start)
        while not exploration_heap.empty():   
            current_waypoint = exploration_heap.get().waypoint  
            if current_waypoint == self.target:
                optimal_route = []
                backtrack = False
                dest_waypoint = self.target.get_coordinates()
                while not backtrack:
                    par_waypoint = parents[str(dest_waypoint)]
                    optimal_route.append(dest_waypoint)
                    dest_waypoint = par_waypoint.get_coordinates()
                    if(par_waypoint == self.start):
                        optimal_route.append(self.start.get_coordinates())
                        backtrack = True
                        break
                optimal_route.reverse()
                return optimal_route
            closed_frontier.append(current_waypoint) 
            for neighbor in current_waypoint.neighbors:
                if not neighbor in closed_frontier:
                    parents[str(neighbor.get_coordinates())] = current_waypoint
                    neighbor_trajectory_cost, neighbor_route_cost = \
                        self.get_trajectory_cost(neighbor)
                    comparable_neighbor = ComparableWaypoint(neighbor_trajectory_cost, neighbor)
                    exploration_heap.put(comparable_neighbor)
                    for viable_waypoint in exploration_heap.queue:
                        waypoint = viable_waypoint.waypoint
                        waypoint_trajectory_cost, waypoint_route_cost = self.get_trajectory_cost(waypoint)
                        if (comparable_neighbor.waypoint.get_coordinates() == waypoint.get_coordinates()):
                            continue
                        elif (neighbor_route_cost <= waypoint_route_cost):
                            if not neighbor in route:
                                parents[str(neighbor.get_coordinates())] = current_waypoint
                                route.append(neighbor)
                else:
                    continue 
        return None

    def get_trajectory_cost(self, waypoint):
        route_cost = 0 # g
        to_target_cost = 0 # h
        trajectory_cost = 0 # f
        route_cost = abs(waypoint.get_coordinates()[0] - self.start.get_coordinates()[0]) \
                     + abs(waypoint.get_coordinates()[1] - self.start.get_coordinates()[1])
        to_target_cost = abs(waypoint.get_coordinates()[0] - self.target.get_coordinates()[0]) \
                     + abs(waypoint.get_coordinates()[1] - self.target.get_coordinates()[1])
        trajectory_cost = route_cost + to_target_cost
        return trajectory_cost, route_cost

    def get_position(self):
        return self.route[int(self.position)%int(len(self.full_route))]

    def get_next_position(self, movement):
        self.position += movement
        return self.get_position()
        
    def get_route(self):
        return self.full_route
    