from node import Node
from sink import Sink
from map import Map


def message_exchange():
    node_1 = Node(id=1)
    node_2 = Node(id=2)
    sink_1 = Sink(id=1)
    sink_2 = Sink(id=2)
    node_1.send_message(receiver=sink_1, message_type="info")
    node_2.send_message(receiver=node_1, message_type="sos")


def map_print():
    map = Map(size=[5,5])
    map.print()
