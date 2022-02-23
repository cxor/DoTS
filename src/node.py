from waypoint import Waypoint
from navigator import Navigator
from queue import Queue
from message import Message
import numpy


class Node:

    LOG = False
    SPECTRUM = 0.65
    MAX_SPEED = 28
    
    def __init__(self, id=0, signal=0, speed=[10,20], \
        mem_capacity=100, navigator=None, fault=0, \
        transmission_rate=10):
        self.id = "node_" + str(id)
        self.status = 1
        self.signal = signal
        self.navigator = navigator
        self.fault = fault
        self.reboot = 5
        self.speed_interval = speed
        self.speed = numpy.random.uniform(speed[0], speed[1])
        self.buffer = Queue(mem_capacity)
        self.no_info_message_received = 0
        self.no_sos_message_received = 0
        self.no_info_message_dropped = 0
        self.no_sos_message_dropped = 0
        self.no_faults = 0
        self.disaster_involved = False

    def get_id(self):
        return self.id

    def get_speed(self):
        return self.speed

    def get_position(self):
        return self.navigator.get_position()
    
    def get_next_position(self, update=False):
        return self.navigator.get_next_position(movement=round(self.speed), update=False)

    def set_position(self, coordinates):
        self.position = coordinates

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
        
    def set_reboot(self, reboot):
        self.reboot = reboot
    
    def get_reboot(self):
        return self.reboot

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, buffer):
        self.buffer = buffer

    def get_navigator(self):
        return self.navigator

    def get_signal(self):
        return self.trx_power

    def set_signal(self, signal):
        return self.signal

    def get_stats(self):
        stats = numpy.array([self.no_info_message_received, 
                            self.no_info_message_dropped,
                            self.no_sos_message_received, 
                            self.no_sos_message_dropped,
                            self.no_faults,
                            self.disaster_involved])
        # Using numpy array to easily ensamblimg stats later
        return stats

    def receive_message(self, message, sensitivity):
        # A message is received if 1. the recipient buffer is
        # not full and 2. the interference does not significantly
        # clog the communication channel.
        sensitivity = numpy.round(sensitivity, 2)
        interference = round(numpy.random.uniform(0,1), 2)
        # TODO: parametrized obstacle random draw
        if Node.LOG:
            print(f"[{message.get_sender_id()}] <-> [{self.id}] sensitivity: {sensitivity}, interference: {interference}")
        if Node.LOG:
            print(f"[{self.id}] ", end="")
        if not (self.buffer.full()) and \
            sensitivity > interference:
            if message.get_type() == "info":
                self.no_info_message_received += 1
            elif message.get_type() == "sos":
                self.no_sos_message_received += 1
            self.buffer.put(message)
            if Node.LOG:
                print(f"received {message.get_type()} message from {message.get_sender_id()}")
        else:
            if message.get_type() == "info":
                self.no_info_message_dropped += 1
            elif message.get_type() == "sos":
                self.no_sos_message_dropped += 1
            if Node.LOG:
                print(f"dropped {message.get_type()} message from {message.get_sender_id()}")
                    
    def get_signal_sensitivity(self, receiver):
        distance = self.get_distance(receiver)
        next_distance = self.get_distance(receiver)
        current_signal_sensitivity = numpy.e ** (-1 * distance / self.signal)
        next_signal_sensitivity = numpy.e ** (-1 * next_distance / self.signal)
        alpha = self.speed / Node.MAX_SPEED
        signal_sensitivity = alpha * next_signal_sensitivity + (1-alpha) * current_signal_sensitivity
        return signal_sensitivity

    def get_next_distance(self, entity):
        x_position = self.get_next_position(update=False)[0]
        y_position = self.get_next_position(update=False)[1]
        if isinstance(entity, Sink):
            x_entity_position = entity.get_position()[0]
            y_entity_position = entity.get_position()[1]
        elif isinstance(entity, Node):
            x_entity_position = entity.get_next_position(update=False)[0]
            y_entity_position = entity.get_next_position(update=False)[1]
        distance = abs(x_position - x_entity_position) \
                   + abs(y_position - y_entity_position)
        return distance
            

    def get_distance(self, entity):
        x_position = self.get_position()[0]
        y_position = self.get_position()[1]
        x_entity_position = entity.get_position()[0]
        y_entity_position = entity.get_position()[1]
        distance = abs(x_position - x_entity_position) \
                   + abs(y_position - y_entity_position)
        return distance

    def send_message(self, receiver, message_type):
        # NOTE: a node attempts to transmit a message whenever
        # it can monitor the presence of a nearby entity. Hence,
        # the stochastic send operation has been replaced, mainly
        # to reduce the number of simulation parameters. As aside,
        # it might be fair to point out that this seems to be the
        # default behaviour in many signalling networks (e.g. SS7,
        # WiFi, ZigBee, Bluetooth, and others).
        # NOTE: it is possible to directly skip some message sends
        if self.id == receiver.get_id():
            return None
        message = Message(sender_id=self.id, receiver_id=receiver.get_id(), \
            message_type=message_type)
        sensitivity = self.get_signal_sensitivity(receiver)
        # if the sensitivity is too low, it means that in a real case
        # scenario the two nodes would be out of reach from each other
        # and we must not consider a message exchange between them
        if sensitivity < Node.SPECTRUM:
            return None
        receiver.receive_message(message=message, sensitivity=sensitivity)
        return None

    def move(self):
        current_position = self.navigator.get_position()
        self.speed = round(numpy.random.uniform(self.speed_interval[0], self.speed_interval[1]), 1)
        movement = self.speed
        next_position = self.navigator.get_next_position(movement)
        if Node.LOG:
            print(f"Node {self.id} is moving from \
            {current_position} to {next_position} with a speed of {movement} m/s")
            
    def crash(self, disaster=False):
        fault_chance = self.fault
        if disaster:
            fault_chance = numpy.random.uniform(0.5, 1-fault_chance)
        fault_happens = numpy.random.uniform(0,1)
        if fault_happens <= fault_chance:
            self.no_faults += 1
            if Node.LOG:
                print(f"Node {self.id} has crashed") 
            return True
        else:
            return False