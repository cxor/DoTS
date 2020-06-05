import numpy as np
import math
import matplotlib.pyplot as plt
from map import Map


def main():
    simulation_map = Map(topology="roads", size=[20,10])
    simulation_map.draw_topology()
    return


if __name__ == "__main__":
    main()