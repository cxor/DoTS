from waypoint import Waypoint
from queue import Queue
from message import Message
import numpy
class Sink:

    LOG = True

    def __init__(self, id=0, coordinates=[-1,-1], \
        signal=15, mem_capacity=100, fault=0):
        self.id = "sink_" + str(id)
        self.position = coordinates
        self.status = 1
        self.signal = signal 
        self.buffer = Queue(mem_capacity)
        self.fault = fault
        self.reboot = 0
        self.no_info_message_received = 0
        self.no_sos_message_received = 0
        self.no_info_message_dropped = 0
        self.no_sos_message_dropped = 0
        self.no_faults = 0

    def get_id(self):
        return self.id

    def get_position(self):
        return self.position
   
    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
        
    def get_buffer(self):
        return self.buffer

    def set_buffer(self, buffer):
        self.buffer = buffer
        
    def get_reboot(self):
        return self.reboot

    def set_reboot(self, reboot):
        self.reboot = reboot

    def get_signal(self):
        return self.signal

    def set_signal(self, signal):
        self.signal = signal

    def get_stats(self):
        stats = numpy.array([self.no_info_message_received,
                            self.no_info_message_dropped,
                            self.no_sos_message_received,
                            self.no_sos_message_dropped,
                            self.no_faults])
        # Using numpy array to easily ensambling stats later
        return stats

    def receive_message(self, message, sensitivity):
        # A message is received if 1. the recipient buffer is
        # not full and 2. the interference does not significantly
        # clog the communication channel.
        sensitivity = numpy.round(sensitivity, 2)
        interference = round(numpy.random.uniform(0,1), 2) 
        if Sink.LOG:
            print(f"[{message.get_sender_id()}] <-> [{self.id}] sensitivity: {sensitivity}, interference: {interference}")
        if Sink.LOG:
            print(f"[{self.id}] ", end="")
        if not self.buffer.full() and \
            sensitivity > interference:
            if message.get_type() == "info":
                self.no_info_message_received += 1
            elif (message.get_type() == "sos"):
                self.no_sos_message_received += 1
            self.buffer.put(message)
            if Sink.LOG:
                print(f"received {message.get_type()} message from {message.get_sender_id()}")
        else:
            if message.get_type() == "info":
                self.no_info_message_dropped += 1
            elif message.get_type() == "sos":
                self.no_sos_message_dropped += 1
            if Sink.LOG:
                print(f"dropped {message.get_type()} message from {message.get_sender_id()}")

    
    def crash(self, disaster=False):
        fault_chance = self.fault
        if disaster:
            fault_chance = numpy.random.uniform(0.5, 1-fault_chance) 
        fault_happens = numpy.random.uniform(0,1)
        if fault_chance <= fault_happens:
            self.no_faults += 1
            if Sink.LOG:
                print(f"Sink {self.id} has crashed") 
            return True
        else:
            return False

            


        

    