import argparse
import sys
import functools

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

def main():
    args = parse()
    show(args)

if __name__ == "__main__":
    main()