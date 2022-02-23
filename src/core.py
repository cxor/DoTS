import test
import sys
import argparse
import functools
from simulator import Simulator
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter

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
    parser.add_argument("-ws", "--working-spectrum", type=bool_float, dest="spectrum", required=False, help="Hard threshold for nodes sensitivity (float, within [0,1])")
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
        

def plot(stats, stats_per_epoch, theoretical_total_msg, no_entities, sim_description):

    fig = plt.figure(figsize=(5.5, 6.5))

    sub1 = fig.add_subplot(2,2,1)
    sub2 = fig.add_subplot(2,2,2)

    msg = ['INFO', 'SOS']
    epoch = range(len(stats_per_epoch))

    info_stats = [stats[0], stats[2]]
    print(stats[2])
    sos_stats = [stats[1], stats[3]]
    labels_info = ['Avg info msg received', 'Avg info msg dropped']
    labels_sos = ['Avg sos msg received', 'Avg sos msg dropped']
    
    sub1.pie(sos_stats, autopct='%1.1f%%', shadow=False, startangle=90, normalize=True, radius=2)
    sub2.pie(info_stats, autopct='%1.1f%%', shadow=False, startangle=90, normalize=True, radius=2)
    
    box = sub1.get_position()
    sub1.set_position([box.x0, box.y0, box.width, box.height*0.6])
    sub1.legend(labels_sos, loc='lower center', bbox_to_anchor=(0.5,1.3))
    box = sub2.get_position()
    sub2.set_position([box.x0, box.y0, box.width, box.height*0.6])
    sub2.legend(labels_info, loc='lower center', bbox_to_anchor=(0.5,1.3))
      
    round_info = []
    avg_info_rcv = []
    avg_sos_rcv = []
    avg_fault_rate = []
    lb_ci_info_rcv = []
    ub_ci_info_rcv = []
    lb_ci_sos_rcv = []
    ub_ci_sos_rcv = []
    lb_ci_fault_rate = []
    ub_ci_fault_rate = []
    entities_involved_disaster = []
    msg_exchanged_vs_theoretical = []
    i_round = []
    for i in epoch:
        round_info.append(f"Round {i+1}\nTotal msg= {stats_per_epoch[i][5]}")
        avg_info_rcv.append(stats_per_epoch[i][0])
        avg_sos_rcv.append(stats_per_epoch[i][1])
        avg_fault_rate.append(stats_per_epoch[i][4])
        lb_ci_info_rcv.append(stats_per_epoch[i][0] if stats_per_epoch[i][0] - stats_per_epoch[i][7] < 0 else stats_per_epoch[i][7])
        ub_ci_info_rcv.append(1-stats_per_epoch[i][0] if stats_per_epoch[i][0] + stats_per_epoch[i][7] > 1 else stats_per_epoch[i][7])
        lb_ci_sos_rcv.append(stats_per_epoch[i][1] if stats_per_epoch[i][1] - stats_per_epoch[i][8] < 0 else stats_per_epoch[i][8])
        ub_ci_sos_rcv.append(1-stats_per_epoch[i][1] if stats_per_epoch[i][1] + stats_per_epoch[i][8] > 1 else stats_per_epoch[i][8])
        lb_ci_fault_rate.append(stats_per_epoch[i][4] if stats_per_epoch[i][4] - stats_per_epoch[i][9] < 0 else stats_per_epoch[i][9])
        ub_ci_fault_rate.append(1-stats_per_epoch[i][4] if stats_per_epoch[i][4] + stats_per_epoch[i][9] > 1 else stats_per_epoch[i][9])
        entities_involved_disaster.append(stats_per_epoch[i][6]/no_entities[i])
        msg_exchanged_vs_theoretical.append(stats_per_epoch[i][5]/theoretical_total_msg[i])
        i_round.append(i+1)
    
    sub3 = fig.add_subplot(2,2,(3,4))
    # this plots the msg exchanges occurred against the theoretical ones 
    sub3.bar(i_round, msg_exchanged_vs_theoretical, width=1, color='tab:gray', label="% msg exchanged vs\ntheoretical total")

    # these plot stats about the average percentage of msg received per simulation
    sub3.plot(i_round, avg_info_rcv, marker='o', color='tab:blue', linestyle='-', label="Avg info msg received")
    sub3.plot(i_round, avg_sos_rcv, marker='o', color='tab:orange', linestyle='-', label="Avg sos msg received")
    
    sub3.plot(i_round, avg_fault_rate, marker='o', color='tab:red', linestyle='-', label="Avg fault rate")
    sub3.errorbar(i_round, avg_info_rcv, yerr=[lb_ci_info_rcv, ub_ci_info_rcv], fmt='.', color='tab:blue', ecolor='tab:blue', capsize=5)
    sub3.errorbar(i_round, avg_sos_rcv, yerr=[lb_ci_sos_rcv, ub_ci_sos_rcv], fmt='.', color='tab:orange', ecolor='tab:orange', capsize=5)
    sub3.errorbar(i_round, avg_fault_rate, yerr=[lb_ci_fault_rate, ub_ci_fault_rate], fmt='.', color='tab:red', ecolor='tab:red', capsize=5)
    sub3.plot(i_round, entities_involved_disaster, marker='.', color='k', linestyle='dotted', label="% nodes involved in\ndisasters")

    sub3.xaxis.set_major_locator(MaxNLocator(integer=True))
    sub3.set_xlabel('# Simulation')
    sub3.set_ylabel('Percentage (%)')
    sub3.set_ylim(top=1.1)
    #axs[1].legend(bbox_to_anchor=(0, 0))
    box = sub3.get_position()
    sub3.set_position([box.x0, box.y0, box.width*0.6, box.height])
    sub3.legend(loc='center left', bbox_to_anchor=(1,0.5))
    sub3.xaxis.set_minor_formatter(FormatStrFormatter(round_info))
    print(sim_description)      #   REMEMBER TO COPY THIS: IT'S FOR THE CAPTION IN THE REPORT
    plt.show()

def main():
    args = parse()
    no_simulations = args.rounds
    stats = numpy.array([.0,.0,.0,.0,.0,.0,.0, .0, .0, .0])
    stats_per_epoch = []
    theoretical_total_msg = []
    no_entities = []
    sim_description = f"Map size {args.map_size}, Duration: {args.duration} seconds, Nodes speed {args.nodes_speed}\n"
    for i in range(no_simulations):
        simulator = Simulator(
            no_nodes=args.nodes_number[i], 
            no_sinks=args.sinks_number[i], 
            node_signal=args.nodes_signal[i],
            sink_signal=args.sinks_signal[i],
            node_speed=args.nodes_speed,
            fault=args.fault_rate[i],
            disaster=args.disaster_rate[i],
            map_size=args.map_size,
            transmission_rate=args.transmission_rate[i],
            duration=args.duration,
            spectrum=args.spectrum)
        simulator.run()
        stats_per_epoch.append(simulator.get_stats())
        stats += simulator.get_stats()
        theoretical_total_msg.append(args.transmission_rate[i]*args.duration*args.nodes_number[i]*(args.nodes_number[i]-1))
        no_entities.append(args.nodes_number[i]+args.sinks_number[i])
        sim_description += f"Sim. {i+1}: {args.nodes_number[i]} nodes, {args.sinks_number[i]}, node signal: {args.nodes_signal[i]}, sink signal: {args.sinks_signal[i]}, transmission rate: {args.transmission_rate[i]} msg/s,\nfault probability: {args.fault_rate[i]}, disaster probability: {args.disaster_rate[i]}\n"
    stats /= no_simulations
    plot(stats, stats_per_epoch, theoretical_total_msg, no_entities, sim_description)

if __name__ == "__main__":
    main()

# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 12 16 --nodes-number 10 20 --sinks-number 7 10 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.1 0.2 --disaster-rate 0.1 0.2 
# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 12 16 --nodes-number 10 20 --sinks-number 7 10 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.4 0.6 --disaster-rate 0.1 0.2 
# python core.py --rounds 2 --duration 1 --map-size 50 50 --nodes-speed 8 13 --nodes-number 20 40 --sinks-number 12 20 --nodes-signal 8 10 --sinks-signal 10 12 --transmission-rate 10 13 --fault-rate 0.05 0.1 --disaster-rate 0.1 0.2
# python core.py --rounds 1 --duration 10 --map-size 50 50 --nodes-speed 8 13 --nodes-number 28 --sinks-number 16 --nodes-signal 9 --sinks-signal 11 --transmission-rate 13 --fault-rate 0.1 --disaster-rate 0.1