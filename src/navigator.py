from waypoint import Waypoint
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class ComparableWaypoint:
    priority: int
    waypoint: Any=field(compare=False)
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
        current_waypoint = self.start       # let openList equal empty list of nodes // put startNode on the openList (leave it's f at zero)
        closed_frontier, route = [], []     # let closedList equal empty list of nodes
        
        comparable_waypoint = \
            ComparableWaypoint(self.get_trajectory_cost(self.start), self.start)
        exploration_heap.put(comparable_waypoint)
        route.append(self.start)
        print(self.start.get_coordinates())
        while not exploration_heap.empty():     # while openList is not empty
            current_waypoint = exploration_heap.get().waypoint  # let currentNode equal the node with the least f value // remove currentNode from the openList
            if current_waypoint == self.target:     # if currentNode is the goal
                return [ waypoint.get_coordinates() for waypoint in route ]     # You've found the exit!
            closed_frontier.append(current_waypoint)    # add currentNode to the closedList
            for neighbor in current_waypoint.get_neighbors():       # for each child in the children
                if neighbor not in closed_frontier:     # if child is not in the closedList
                    neighbor_trajectory_cost, neighbor_route_cost = \
                        self.get_trajectory_cost(neighbor)        # child.g, child.h, child.f
                    comparable_neighbor = ComparableWaypoint(neighbor_trajectory_cost, neighbor)
                    exploration_heap.put(comparable_neighbor)
                    for viable_waypoint in exploration_heap.queue:
                        # Get the waypoint attribute in ComparableWaypoint dataclass
                        waypoint = viable_waypoint.waypoint
                        waypoint_trajectory_cost, waypoint_route_cost = self.get_trajectory_cost(waypoint)
                        for item in exploration_heap.queue:
                            if (comparable_neighbor.waypoint.get_coordinates() == item.waypoint.get_coordinates()):
                                pass
                            elif (neighbor_route_cost <= waypoint_route_cost):
                                route.append(neighbor)
                                
                else:
                    continue        # continue to beginning of for loop
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
        return self.position

    def get_route(self):
        return self.route
    