from simulator import Simulator
import test

def launch_batch_simulations():
    no_batch_simulations = 3
    no_nodes = [50, 100, 200]
    no_sinks = [25, 50, 100]
    node_signal = [15, 12, 10]
    sink_signal = [20, 17, 15]
    node_speed = [12, 24, 36]
    fault = [0.1, 0.3, 0.4]
    disaster = [0, 0.1, 0.2]
    map_size = [100, 100]
    map_scale = 2
    simulation_epochs = 20 
    # -----------------------------------
    for i in range(no_batch_simulations):
        simulator = Simulator(          \
            no_nodes=no_nodes[i],       \
            no_sinks=no_sinks[i],       \
            node_signal=node_signal[i], \
            sink_signal=sink_signal[i], \
            node_speed=node_speed[i],   \
            fault=fault[i],             \
            disaster=disaster[i],       \
            map_size=map_size,          \
            map_scale=map_scale)
        simulator.run(epochs=simulation_epochs)
        simulator.plot()

def main():
    test.message_exchange()

if __name__ == "__main__":
    main()