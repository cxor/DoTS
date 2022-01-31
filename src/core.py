import test
import sys
import argparse
import functools
from simulator import Simulator
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator

def preparse():
    # Brief preprocessing needed to extrapolate arguments needed as
    # parameter definition for other user given arguments.
    preproc = argparse.ArgumentParser(add_help=False)
    preproc.add_argument("-r", "--rounds", type=int, dest="rounds", default=1)
    meta_args = preproc.parse_known_args()[0]   # meta_args = (known_args, unknown_args)
    return meta_args

def parse():
    # -----------------------------------------------------------
    def range_check(value, min, max):
        try:
            value = float(value)
        except ValueError as error:
           raise argparse.ArgumentTypeError(str(error))
        if value < min or value > max:
            message = "Input value {} out of range".format(value)
            raise argparse.ArgumentTypeError(message)
        return value
    # -----------------------------------------------------------
    bool_float = functools.partial(range_check, min=0, max=1)
    meta_args = preparse()
    rounds = meta_args.rounds
    parser = argparse.ArgumentParser(                   \
        prog="dots", usage="%{prog}s [options]",     \
        description="DoTS: delay-tolerant network simulator")
    parser.add_argument("-r", "--rounds", type=int, dest="rounds", default=1, required=True, help="Number of simulation rounds")
    parser.add_argument("-nn", "--nodes-number", type=int, dest="nodes_number", required=True, nargs=rounds, help="Number of nodes")
    parser.add_argument("-sn", "--sinks-number", type=int, dest="sinks_number", required=True, nargs=rounds, help="Number of sinks")
    parser.add_argument("-ns", "--nodes-signal", type=float, dest="nodes_signal", required=True, nargs=rounds, help="Nodes signal transmission power (float, dBm)")
    parser.add_argument("-ss", "--sinks-signal", type=float, dest="sinks_signal", required=True, nargs=rounds, help="Sinks signal transmission power (float, dBm)")
    parser.add_argument("-sp", "--nodes-speed", type=float, dest="nodes_speed", required=True, nargs=2, help="Nodes movement speed ((min,max) float, m/s)")
    parser.add_argument("-tr", "--transmission-rate", type=int, dest="transmission_rate", required=True, nargs=rounds, help="Transmission rate for nodes (pkt/s)")
    parser.add_argument("-fr", "--fault-rate", type=bool_float, dest="fault_rate", required=True, nargs=rounds, help="Probability of a unrecoverable software problem (float, within [0,1])")
    parser.add_argument("-dr", "--disaster-rate", type=bool_float, dest="disaster_rate", required=True, nargs=rounds, help="Probability of a natural disaster (float, within [0,1])")
    parser.add_argument("-mp", "--map-size", type=int, dest="map_size", required=True, nargs=2, help="Map size: length, width (int, meters)")
    parser.add_argument("-d", "--duration", type=int, dest="duration", required=True, help="Simulation duration (int, seconds)")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Show detailed simulation log")
    parser.add_argument("-p", "--plot", action="store_true", default=False, help="Plot the simulation results")
    args = parser.parse_args()
    return args
    

def show(args):
    print("*** Simulation outline ***")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Simulation epochs: " + str(args.rounds))
    print("Nodes number: " + str(args.nodes_number))
    print("Sinks number: " + str(args.sinks_number))
    print("Nodes signal power: " + str(args.nodes_signal))
    print("Sinks signal power: " + str(args.sinks_signal))
    print("Nodes speed: " + str(args.nodes_speed))
    print("Transmission rate: " + str(args.transmission_rate))
    print("Fault rate: " + str(args.fault_rate))
    print("Disaster rate: " + str(args.disaster_rate))
    print("Map size: " + str(args.map_size))
    print("Simulation duration: " + str(args.duration))
    if args.verbose:
        print("Simulation log: YES")
    else:
        print("Simulation log: NO")
    if args.plot:
        print("Plot results: YES")
    else:
        print("Plot results: NO")
        

def plot(stats, stats_per_epoch):
    fig, axs = plt.subplots(2)
    
    msg = ['INFO', 'SOS']
    epoch = range(len(stats_per_epoch))
    width = 0.1

    axs[0].bar(msg[0], stats[2], width, color='r')
    axs[0].bar(msg[0], stats[0], width, bottom=stats[2], color='b')
    axs[0].bar(msg[1], stats[3], width, color='r')
    axs[0].bar(msg[1], stats[1], width, bottom=stats[3], color='b')
    
    axs[0].legend(labels=['Dropped', 'Received'])

    for i in epoch:
        axs[1].plot(i, stats_per_epoch[i][0], marker='o', color='r', linestyle='-')
        axs[1].plot(i, stats_per_epoch[i][1], marker='o', color='b', linestyle='-')
        axs[1].plot(i, stats_per_epoch[i][2], marker='o', color='y', linestyle='-')
        axs[1].plot(i, stats_per_epoch[i][3], marker='o', color='g', linestyle='-')
        axs[1].plot(i, stats_per_epoch[i][4], marker='o', color='c', linestyle='-')

    axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Average')
    axs[1].legend(bbox_to_anchor=(0, 0))
    axs[1].legend(labels=['Avg info msg received', 
                          'Avg sos msg received',
                          'Avg info msg dropped',
                          'Avg sos msg dropped',
                          'Avg fault rate'])
    plt.show()

def main():
    args = parse()
    no_simulations = args.rounds
    stats = numpy.array([.0,.0,.0,.0,.0])
    stats_per_epoch = []
    for i in range(no_simulations):
        simulator = Simulator(
            no_nodes=args.nodes_number[i], 
            no_sinks=args.sinks_number[i], 
            node_signal=args.nodes_signal[i],
            sink_signal=args.sinks_signal[i],
            node_speed=args.nodes_speed[i],
            fault=args.fault_rate[i],
            disaster=args.disaster_rate[i],
            map_size=args.map_size,
            transmission_rate=args.transmission_rate[i],
            duration=args.duration)
        simulator.run()
        stats_per_epoch.append(simulator.get_stats())
        print(str(stats_per_epoch))
        stats += simulator.get_stats()
    stats /= no_simulations
    plot(stats, stats_per_epoch)

if __name__ == "__main__":
    main()

# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 12 16 --nodes-number 10 20 --sinks-number 7 10 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.1 0.2 --disaster-rate 0.1 0.2 
# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 12 16 --nodes-number 10 20 --sinks-number 7 10 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.4 0.6 --disaster-rate 0.1 0.2 
# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 8 13 --nodes-number 20 40 --sinks-number 12 20 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.05 0.1 --disaster-rate 0.1 0.2
# python core.py --rounds 1 --duration 10 --map-size 50 50 --nodes-speed 8 13 --nodes-number 28 --sinks-number 16 --nodes-signal 9 --sinks-signal 11 --transmission-rate 13 --fault-rate 0.1 --disaster-rate 0.1