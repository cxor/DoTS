from waypoint import Waypoint
from navigator import Navigator
from queue import Queue
from message import Message
import numpy
class Node:

    LOG = True
    
    def __init__(self, id=0, signal=0, speed=0, \
        mem_capacity=100, navigator=None, fault=0):
        self.id = "node_" + str(id)
        self.status = 1
        self.signal = signal
        self.navigator = navigator
        self.fault = fault
        self.speed = round(numpy.random.uniform(speed/2, speed), 1)
        self.buffer = Queue(mem_capacity)
        self.no_info_message_received = 0
        self.no_sos_message_received = 0
        self.no_info_message_dropped = 0
        self.no_sos_message_dropped = 0

    def get_id(self):
        return self.id

    def get_speed(self):
        return self.speed

    def get_position(self):
        return self.navigator.get_position()

    def set_position(self, coordinates):
        self.position = coordinates

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

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
        stats = numpy.array[self.no_info_message_received, 
                            self.no_info_message_dropped,
                            self.no_sos_message_received, 
                            self.no_sos_message_received]
        # Using numpy array to easily ensamblimg stats later
        return stats

    def receive_message(self, message, sensitivity):
        # A message is received if 1. the recipient buffer is
        # not full and 2. the interference does not significantly
        # clog the communication channel.
        interference = round(numpy.random.uniform(0,1), 2)
        # TODO: parametrized obstacle rnadom draw
        if Node.LOG:
            print(f"[{self.id}] ", end="")
            if not (self.buffer.full()) and \
                sensitivity < interference:
                if message.get_type() == "info":
                    self.no_info_message_received += 1
                elif message.get_type() == "sos":
                    self.no_sos_message_received += 1
                self.buffer.put(message)
                if Node.LOG:
                    print(f"received {message.get_type()} \
                        message from {message.get_sender_id()}")
            else:
                if message.get_type() == "info":
                    self.no_info_message_dropped += 1
                elif message.get_type() == "sos":
                    self.no_sos_message_dropped += 1
                if Node.LOG:
                    print(f"dropped {message.get_type()} \
                    message from {message.get_sender_id()}")
                    
    def get_signal_sensitivity(self, receiver):
        # TODO: implement here the sensitivity metrics
        pass

    def send_message(self, receiver, message_type):
        # NOTE: a node attempts to transmit a message whenever
        # it can monitor the presence of a nearby entity. Hence,
        # the stochastic send operation has been replaced, mainly
        # to reduce the number of simulation parameters. As aside,
        # it might be fair to point out that this seems to be the
        # default behaviour in many signalling networks (e.g. SS7,
        # WiFi, ZigBee, Bluetooth, and others).
        # NOTE: it is possible to directly skip some message sends
        message = Message(sender_id=self.id, receiver_id=receiver.get_id(), \
            message_type=message_type)
        sensitivity = self.get_signal_sensitivity(receiver)
        receiver.receive_message(message=message, sensitivity=sensitivity)
