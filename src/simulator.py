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
        # its value is equal to the probability of having entity/sink
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
        self.nodes = map.get_entitys()
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
            if disaster_happens:
                Simulator.simulate_disaster(map, self.nodes, self.sinks)
            Simulator.simulate_fault(fault_epochs, disaster_happens)
            map.update(disaster=disaster_happens)
            Simulator.simulate_reboot()
            
    def simulate_fault(self, fault_epochs, disaster_happens):
        for entity in self.nodes+self.sinks:
            if entity.crash(disaster_happens):
                entity.set_status(0)
                entity.set_reboot(fault_epochs)

    def simulate_reboot(self):
        for entity in self.nodes+self.sinks:
            if entity.get_status() == 0:
                reboot_elapsed_time = entity.get_reboot()
                if reboot_elapsed_time == 0:
                    entity.set_status(1)
                else:
                    entity.set_reboot(reboot_elapsed_time - 1)
                
    def simulate_disaster(self, map, disaster_epochs):
        map_size = map.get_size()
        disaster_radius = round(numpy.random.uniform(1, min(map_size)//2))
        disaster_x_epicenter = round(numpy.random.uniform(1, map_size[0]))
        disaster_y_epicenter = round(numpy.random.uniform(1, map_size[1]))
        disaster_min_coord = \
            (max(0, disaster_x_epicenter-disaster_radius),
            max(0, disaster_y_epicenter-disaster_radius))
        disaster_max_coord = \
            (min(map_size[0]-1, disaster_x_epicenter+disaster_radius),
            min(map_size[1]-1, disaster_y_epicenter+disaster_radius))
        for entity in self.nodes+self.sinks:
            entity_x_coord = entity.get_position()[0]
            entity_y_coord = entity.get_position()[1]
            if (disaster_min_coord[0] <= entity_x_coord) \
                and (entity_x_coord <= disaster_max_coord[0]) \
                and (disaster_min_coord[1] <= entity_y_coord) \
                and (entity_y_coord <= disaster_max_coord[1]):
                    if entity.crash(disaster=True):
                        entity.set_status(0)
                        entity.set_reboot(disaster_epochs)



    def plot(self):
        pass