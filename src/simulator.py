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
        self.map_size = (map_size[0]//self.map_scale, map_size[1]//self.map_scale)
        self.nodes = []
        self.sinks = []
        self.stats = numpy.array([0, 0, 0, 0, 0, 0])

    def run(self, seconds=10):
        map = Map(self.no_nodes, self.no_sinks, self.node_signal, \
                  self.sink_signal, self.node_speed, self.fault, \
                  self.transmission_rate, self.map_size)
        self.nodes = map.get_nodes()
        self.sinks = map.get_sinks()
        epochs = int(seconds * self.transmission_rate)
        disaster_epochs = epochs // 10
        fault_epochs = epochs // 50
        disaster_counter = disaster_epochs
        disaster_happens = False

        for _ in range(epochs):
            if disaster_happens:
                if disaster_counter > 0:
                    disaster_chance = 1 
                else:
                    disaster_happens = False
                    disaster_counter = disaster_epochs
                    disaster_chance = numpy.random.uniform(0,1)
            else:
                disaster_chance = numpy.random.uniform(0,1)
            if disaster_chance >= 1 - self.disaster:
                disaster_happens = True
                disaster_counter -= 1
            Simulator.simulate_fault(fault_epochs, disaster_happens)
            map.update(disaster=disaster_happens)
            Simulator.simulate_reboot()
            
    def simulate_fault(self, fault_epochs, disaster_happens):
        for node in self.nodes:
            if node.simulate_fault(disaster_happens):
                node.set_status(0)
                node.set_reboot(fault_epochs)
        for sink in self.sinks:
            if sink.simulate_fault(disaster_happens):
                sink.set_status(0)
                sink.set_reboot(fault_epochs)

    def simulate_reboot(self):
        for node in self.nodes:
            reboot_elapsed_time = node.get_reboot()
            if reboot_elapsed_time == 0:
                node.set_status(1)
            else:
                node.set_reboot(reboot_elapsed_time - 1)
        for sink in self.sinks:
            reboot_elapsed_time = sink.get_reboot()
            if reboot_elapsed_time == 0:
                sink.set_status(1)
            else:
                sink.set_reboot(reboot_elapsed_time - 1)
                
    def simulate_disaster(self, nodes, sinks, disaster_happens):
        # Select a random point in the map
        # Build the maximum area coordinates
        # For each entity, check if it is in the area
        # Set the entity status to 2
        pass

    def plot(self):
        pass