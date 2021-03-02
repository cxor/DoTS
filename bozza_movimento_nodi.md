Since we were to simulate a delay tolerant network with nodes moving in a given environment, the first thing to implement was the movement of the nodes. We decided that each node would have a fixed path that it would periodically walk upon. Each node has a starting point (`Node.start`) to the path and an ending point (`Node.target`). The path is chosen during the setup of the scenario with A* algorithm.

We decided to have the nodes following periodically a fixed path so to emulate an everyday life scenario, e.g. a person going to work and then going back home.

A limit on the number of nodes has been imposed w.r.t the number of available spaces on the map, so to not have a too many or too few of them. Both the starting position and the target one are randomly chosen.