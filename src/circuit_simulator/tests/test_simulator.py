import pytest
import os
from circuit_simulator import CircuitSimulator
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt


def plot_simulation_results(x_values_sim, y_values_sim, ground_truth_data, node, circuit_name, sim_plot_folder):
    plt.figure()
    plt.plot(ground_truth_data.index.values, ground_truth_data[f"{node}"].values, label="Ground Truth")
    plt.plot(x_values_sim, y_values_sim, label="Simulation", linestyle='dashed')
    plt.xlabel("Time")
    plt.ylabel(f"Node {node} (V)")
    plt.title(f"Ground Truth Vs Sim {circuit_name} Node {node}")
    plt.legend(["Ground Truth", "Simulation"])
    plt.savefig(f'{sim_plot_folder}/node_{node}_ground_truth.png')
    plt.close()


def plot_ground_truth(ground_truth_data, node, circuit_name, ground_truth_plot_folder):
    plt.figure()
    plt.plot(ground_truth_data.index.values, ground_truth_data[f"{node}"].values)
    plt.xlabel("Time")
    plt.ylabel(f"Node {node} (V)")
    plt.title(f"Ground Truth {circuit_name} Node {node}")
    plt.savefig(f'{ground_truth_plot_folder}/node_{node}_ground_truth.png')
    plt.close()


def read_ground_truth(gt_path):
    return pd.read_csv(gt_path, sep=r'\s+', index_col=0)

@pytest.mark.parametrize("circuit_name, atol",
    [
        ("chua", 8e-2),
        ("lc", 5e-5),
        ("sinusoidal", 1e-6),
        ("pulse", 1e-6),
        ("dc_source", 1e-6),
        ("oscilator", 1e-3),
        ("opamp_rectifier", 3e-5),
        ("mosfet_curve", 3e-6),
])
class TestCircuitSimulator:

    def test_netlist(self, circuit_name, atol):
        """Test the CircuitSimulator with the Chua's circuit netlist."""

        ##########################################
        # Reading Ground Truth Data
        ##########################################
        
        netlist_path = f'../netlists/examples/{circuit_name}.net'
        ground_truth_path = f'../netlists/examples/ground_truth/{circuit_name}.sim'
        ground_truth_data = read_ground_truth(ground_truth_path)
        
        # Get expected number of nodes
        total_nodes = 0
        for col in ground_truth_data.columns:
            try:
                int(col)
                total_nodes += 1
            except ValueError:
                pass

        ##########################################
        # Generating Simulation Data
        ##########################################
        simulator = CircuitSimulator(
            mode="netlist",
            netlist_path=netlist_path,
        )
        simulator.run()
        x_values_sim = np.round(simulator.steps, 5)  # Convert to ms

        
        ##########################################
        # Debugging before assert in case of Error
        ##########################################
        print(f"\n\n--- Testing circuit: {circuit_name} ---")
        print("Total nodes in ground truth data:", total_nodes)  

        # Debug: Expected values
        print("Ground Truth TIME:", ground_truth_data.index.values)
        print("Simulation TIME:", x_values_sim)
        print("len(ground_truth_data):", len(ground_truth_data.index.values))
        print("len(Simulation TIME):", len(x_values_sim))
        print("Difference_time:", ground_truth_data.index.values - x_values_sim)
        print("\n\n")
        
        # Debug: Print for Debugging the maximum difference
        max_diff_index = np.argmax(np.abs(ground_truth_data.index.values - x_values_sim))
        print(f"Índice do maior valor absoluto da diferença: {max_diff_index}")
        print("Valor no Ground Truth nesse índice:", ground_truth_data.index.values[max_diff_index])
        print("Valor na Simulação nesse índice:", x_values_sim[max_diff_index])
        print("Maior valor absoluto da diferença:", np.max(np.abs(ground_truth_data.index.values - x_values_sim)))

        ##########################################
        # Assert Time Values
        ##########################################
        assert len(ground_truth_data.index.values) == len(x_values_sim), "Output length mismatch"
        assert np.allclose(x_values_sim, ground_truth_data.index.values, atol=atol), "Time values mismatch"
        
        for node in range(1, total_nodes + 1):
            ################################################
            # Get Simulation Node Values
            ################################################
            y_values_sim = np.round(simulator.answer[:, node], 6)  # Node 1 voltage
            
            ####################################################
            # Save Plots Ground Truth and Simulation Node Values
            ####################################################
            ground_truth_plot_folder = f'circuit_simulator/tests/plots/{circuit_name}/ground_truth_plots'
            sim_plot_folder = f'circuit_simulator/tests/plots/{circuit_name}/sim_plots'
            os.makedirs(ground_truth_plot_folder, exist_ok=True)
            os.makedirs(sim_plot_folder, exist_ok=True)
            plot_simulation_results(x_values_sim, y_values_sim, ground_truth_data, node, circuit_name, sim_plot_folder)
            plot_ground_truth(ground_truth_data, node, circuit_name, ground_truth_plot_folder)


            ##########################################
            # Debugging before assert in case of Error
            ##########################################
            print(f"\n\n--- Node {node} ---")
            print("Ground Truth Value:", ground_truth_data[f"{node}"])
            print("\nSimulation Value:", y_values_sim)
            print("Difference_Value:", ground_truth_data[f"{node}"].values - y_values_sim)
            
            # Debug: Print for Debugging the maximum difference
            max_diff_index = np.argmax(np.abs(ground_truth_data[f"{node}"].values - y_values_sim))
            print(f"Índice do maior valor absoluto da diferença: {max_diff_index}")
            print("Valor no Ground Truth nesse índice:", ground_truth_data[f"{node}"].values[max_diff_index])
            print("Valor na Simulação nesse índice:", y_values_sim[max_diff_index])
            print("Maior valor absoluto da diferença:", np.max(np.abs(ground_truth_data[f"{node}"].values - y_values_sim)))


            ##########################################
            # Assert Node Values
            ##########################################
            # Assert node values with tolerance
            msg = f"Ground Truth Value: {ground_truth_data[f"{node}"]} \nSimulation Value: {y_values_sim}"
            assert np.allclose(y_values_sim, ground_truth_data[f"{node}"], atol=atol), \
                    f"Node {node} values mismatch. \n{msg}"
            