from map import Map
from navigator import Navigator
from node import Node
from sink import Sink
import numpy
import random
import time
from scipy.stats import norm


class Simulator:

    LOG = True
    REBOOT_TIME = 5
    
    def __init__(self,no_nodes, no_sinks, node_signal,\
        sink_signal, node_speed=[10,20], fault=0, disaster=0, \
        map_size=[100,100], transmission_rate=10, duration=5, spectrum=0.65):
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
        self.map_scale = self.time_scale * self.node_speed[0]
        self.map_size = (map_size[0]//self.map_scale, map_size[1]//self.map_scale)
        self.map = Map(size=map_size, no_active_locations=no_nodes+no_sinks)
        self.duration = duration
        self.nodes = []
        self.sinks = []
        self.epochs = int(duration * transmission_rate)
        self.epoch_counter = 0
        self.stats = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.disaster_overlay = numpy.array([0, 0, 0, 0])

    def get_entities_params(self):
        return self.no_nodes, self.no_sinks, self.node_signal, self.sink_signal,\
            self.node_speed, self.transmission_rate

    def get_map(self):
        return self.map

    def get_nodes(self):
        return self.nodes

    def get_sinks(self):
        return self.sinks
    
    def get_stats(self):
        return self.stats

    def get_disaster_overlay(self):
        return self.disaster_overlay
    
    def populate(self):
        # NOTE: Network generation happens automatically 
        # whenever a new map is instanciated
        if Simulator.LOG:
            print("Preparing simulation map...")
        # --- Populate with sinks ---
        available_positions = self.map.get_available_positions()
        sink_locations = random.sample(available_positions, self.no_sinks)
        for i in range(self.no_sinks):
            current_waypoint = sink_locations[i]
            sink = Sink(id=i, coordinates=current_waypoint.get_coordinates(), \
                signal=self.sink_signal, fault=self.fault)
            self.sinks.append(sink)
            if Simulator.LOG:
                print(f"Activating entity: sink_{i}")
        # --- Populate with nodes ---
        available_positions = self.map.get_available_positions()
        node_locations = random.sample(available_positions, self.no_nodes)
        node_targets = random.sample(available_positions, self.no_nodes)
        for i in range(self.no_nodes):
            start_waypoint = node_locations[i]
            target_waypoint = node_targets[i]
            navigator = Navigator(start=start_waypoint, \
                target=target_waypoint, network=self.map.get_network())
            node = Node(id=i, signal=self.node_signal, speed=self.node_speed, \
                    navigator=navigator, fault=self.fault, \
                    transmission_rate=self.transmission_rate, \
                    time_scale=self.time_scale)
            self.nodes.append(node)
            if Simulator.LOG:
                print(f"Activating entity: node_{i}")
        if Simulator.LOG:
            print("--> Simulation map prepared.")


    def run(self):
        self.populate()
        # self.nodes, self.sinks filled
        disaster_epochs = int(numpy.random.uniform(1, self.epochs))
        disaster_counter = int(disaster_epochs)
        disaster_happens = False

        for i in range(self.epochs):
            if disaster_happens: # 4
                if disaster_counter >= 0: # 5.1
                    disaster_chance = 1 
                else: # 5.2
                    disaster_happens = False
                    disaster_epochs = int(numpy.random.uniform(1, self.epochs - i))
                    disaster_counter = int(disaster_epochs)
                    disaster_chance = numpy.random.uniform(0,1)
            else: # 4.1 / 0
                disaster_chance = numpy.random.uniform(0,1)
            # -----------------------------------------------------------------------------
            if disaster_chance >= 1 - self.disaster:
                # The code here executes when a disaster is on
                disaster_happens = True # 1
                if Simulator.LOG:
                    print("A disaster has begun!")
                if disaster_counter == disaster_epochs: # 2
                    # Here starts the disaster
                    self.disaster_overlay = self.create_disaster_overlay()
                disaster_counter -= 1 # 3
            # -----------------------------------------------------------------------------
            if Simulator.LOG:
                print("Simulation epoch no. " + str(i) + "/" + str(self.epochs))
                #time.sleep(0.1)
            self.update(disaster=disaster_happens)
            
    def simulate_fault(self, disaster_happens=False):
        for entity in self.nodes+self.sinks:
            if entity.get_status() == 1 :
                if entity.crash(disaster_happens):
                    entity.set_status(0)

    def simulate_reboot(self):
        for entity in self.nodes+self.sinks:
            if entity.get_status() == 0:
                reboot_elapsed_time = entity.get_reboot()
                if reboot_elapsed_time == 0:
                    entity.set_status(1)
                    entity.set_reboot(Simulator.REBOOT_TIME)
                else:
                   # entity.no_faults += 1
                    entity.set_reboot(reboot_elapsed_time - 1)
                
    def simulate_disaster(self):
        disaster_min_x_coord = self.disaster_overlay[0]
        disaster_min_y_coord = self.disaster_overlay[1]
        disaster_max_x_coord = self.disaster_overlay[2]
        disaster_max_y_coord = self.disaster_overlay[3]
        for entity in self.nodes+self.sinks:
            entity_x_coord = entity.get_position()[0]
            entity_y_coord = entity.get_position()[1]
            if (disaster_min_x_coord <= entity_x_coord) \
                and (entity_x_coord <= disaster_max_x_coord) \
                and (disaster_min_y_coord <= entity_y_coord) \
                and (entity_y_coord <= disaster_max_y_coord):
                    entity.disaster_involved=True
                    if entity.crash(disaster=True):
                        entity.set_status(0)
                    else:
                        entity.set_status(-1)
    
    def create_disaster_overlay(self):
        map_size = self.map.get_size()
        disaster_radius = round(numpy.random.uniform(1, min(map_size)//2))
        disaster_x_epicenter = round(numpy.random.uniform(1, map_size[0]))
        disaster_y_epicenter = round(numpy.random.uniform(1, map_size[1]))
        disaster_min_coord = \
            (max(0, disaster_x_epicenter-disaster_radius),
            max(0, disaster_y_epicenter-disaster_radius))
        disaster_max_coord = \
            (min(map_size[0]-1, disaster_x_epicenter+disaster_radius),
            min(map_size[1]-1, disaster_y_epicenter+disaster_radius))
        return \
            disaster_min_coord[0],      \
            disaster_min_coord[1],      \
            disaster_max_coord[0],      \
            disaster_max_coord[1]

    def simulate_movement(self):
        for node in self.nodes:
            if node.get_status != 0:
                node.move()
    
    def simulate_communication(self):
        for node in self.nodes:
            node_status = node.get_status()
            if node_status == 0:
                if Node.LOG:
                    print(f"[{node.get_id()}] is unable to communicate (FAULT status probed)")
                    continue
            msg_type = "debug"
            if node_status == 1:
                msg_type = "info"
            elif node_status == -1:
                msg_type = "sos"
            for receiver in self.nodes+self.sinks:
                node.send_message(receiver, msg_type)
                
    def update(self, disaster):
        self.epoch_counter += 1
        if disaster:
            self.simulate_disaster()
        self.simulate_fault() 
        self.simulate_reboot()
        self.simulate_movement()
        self.simulate_communication()

    def get_stats(self):
        eta = norm.ppf((1 + 0.99) / 2)
        no_info_msg_received = 0
        no_sos_msg_received = 0
        no_info_msg_dropped = 0
        no_sos_msg_dropped = 0
        no_faults = 0
        no_involved_in_disasters = 0
        for entity in self.nodes + self.sinks:
            stats = entity.get_stats()
            no_info_msg_received += stats[0]
            no_sos_msg_received += stats[2]
            no_info_msg_dropped += stats[1]
            no_sos_msg_dropped += stats[3]
            no_faults += stats[4]
            if stats[5]:
                no_involved_in_disasters += 1
        no_entities = len(self.nodes)+len(self.sinks)
        no_epochs_elapsed = self.epoch_counter
        no_info_msg = no_info_msg_received + no_info_msg_dropped
        no_sos_msg = no_sos_msg_received + no_sos_msg_dropped
        no_msg = no_info_msg + no_sos_msg
        
        no_faults_avg = 0 if no_faults == 0 else (no_faults / no_entities) / no_epochs_elapsed 
        no_faults_sd = 0 if no_faults == 0 else no_faults_avg - (no_faults_avg ** 2)
        no_faults_ci = eta * ((no_faults_sd ** 0.5) / (no_epochs_elapsed ** 0.5))
        # no_info_msg_received_avg = no_info_msg_received / no_info_msg
        no_info_msg_received_avg = 0 if no_info_msg == 0 else no_info_msg_received / no_info_msg
        no_info_msg_received_sd = 0 if no_info_msg == 0 else no_info_msg_received_avg - (no_info_msg_received_avg ** 2)
        no_info_msg_received_ci = eta * ((no_info_msg_received_sd ** 0.5) / (no_info_msg ** 0.5))
        # no_sos_msg_received_avg = no_sos_msg_received / no_sos_msg
        no_sos_msg_received_avg = 0 if no_sos_msg == 0 else no_sos_msg_received / no_sos_msg
        no_sos_msg_received_sd = 0 if no_sos_msg == 0 else no_sos_msg_received_avg - (no_sos_msg_received_avg ** 2)
        no_sos_msg_received_ci = eta * ((no_sos_msg_received_sd ** 0.5) / (no_sos_msg ** 0.5))
        # no_info_msg_dropped_avg = no_info_msg_dropped / no_info_msg
        no_info_msg_dropped_avg = 0 if no_info_msg == 0 else no_info_msg_dropped / no_info_msg
        no_info_msg_dropped_sd = 0 if no_info_msg == 0 else no_info_msg_dropped_avg - (no_info_msg_dropped_avg **2)
        no_info_msg_dropped_ci = eta * ((no_info_msg_dropped_sd ** 0.5) / (no_info_msg ** 0.5))
        #no_sos_msg_dropped_avg = no_sos_msg_dropped / no_sos_msg
        no_sos_msg_dropped_avg = 0 if no_sos_msg == 0 else no_sos_msg_dropped / no_sos_msg
        no_sos_msg_dropped_sd = 0 if no_sos_msg == 0 else no_sos_msg_dropped_avg - (no_sos_msg_dropped_avg **2)
        no_sos_msg_dropped_ci = eta * ((no_sos_msg_dropped_sd ** 0.5) / (no_sos_msg ** 0.5))
        # no_faults_avg = (no_faults / no_entities) / no_epochs
        if Simulator.LOG:
            print("*** Simulation statistics ***")
            print("+──────────────────────────────────────────────+")
            print("Total message exchange attempts: " + str(no_msg))
            print("Total info messages: " + str(no_info_msg))
            print("Total sos messages: " + str(no_sos_msg))
            print("Average info message received: " + str(no_info_msg_received_avg))
            print("s.dev^2 info message received: " + str(no_info_msg_received_sd))
            print("CI info message received: " + str(no_info_msg_received_ci))
            print("Average sos message received: " + str(no_sos_msg_received_avg))
            print("Average fault rate: " + str(no_faults_avg))
            print("Entities involved in disasters: " + str(no_involved_in_disasters))
            print("+──────────────────────────────────────────────+")
        stats = numpy.array(
            [no_info_msg_received_avg,  \
            no_sos_msg_received_avg,    \
            no_info_msg_dropped_avg,    \
            no_sos_msg_dropped_avg,     \
            no_faults_avg,              \
            no_msg,                     \
            no_involved_in_disasters,   \
            no_info_msg_received_ci,    \
            no_sos_msg_received_ci,     \
            no_faults_ci])
        return stats