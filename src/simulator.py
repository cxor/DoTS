from map import Map
import numpy

class Simulator:
    
    def __init__(self,no_nodes, no_sinks, node_signal,\
        sink_signal, node_speed=10, fault=0, disaster=0, \
        map_size=[100,100], transmission_rate=10):
        self.no_nodes = no_nodes
        self.no_sinks = no_sinks
        self.node_signal = node_signal
        self.sink_signal = sink_signal
        self.node_speed = node_speed
        self.transmission_rate = transmission_rate
        # The disaster parameters regulates the rate of disasters
        # and is bounded by a [0,1] interval, with 0 meaning no
        # disaster, and 1 representing a continous disastered stage.
        # A value of 0.5 yields a probability of 50% to experience a
        # disaster every simulation run. 
        # The fault parameter follows an equivalent behaviour, where 
        # its value is equal to the probability of having node/sink
        # crashes during every run of a simulation.
        self.fault = fault
        self.disaster = disaster
        self.time_scale = 1 / self.transmission_rate
        self.map_scale = self.time_scale * self.node_speed
        self.map_size = map_size / self.map_scale
        self.stats = numpy.array([0, 0, 0, 0])

    def run(self, epochs=10):
        # TODO: load the parameters to build the maps
        map = Map(size=self.map_size)
        map.build(self.no_nodes, self.no_sinks, self.node_signal, \
           self.sink_signal, self.fault, self.transmission_rate)

        for i in range(epochs):
            disaster = False
            disaster_chance = numpy.random.uniform(0,1)
            if disaster_chance <= self.disaster:
                disaster = True
            map.update(disaster=disaster)
            
    def plot(self):
        pass