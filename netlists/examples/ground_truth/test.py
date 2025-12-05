import pandas as pd
from CircuitSimulator import CircuitSimulator


def read_ground_truth(gt_path):
    return pd.read_csv(gt_path, delim_whitespace=True, index_col=0)

netlist_path = '../../netlists/examples/sinusoidal.net'

ground_truth_path = '../../netlists/examples/ground_truth/sinusoidal.sim'
ground_truth_path = './sinusoidal.sim'
ground_truth_data = read_ground_truth(ground_truth_path)
print(ground_truth_data["1"])

simulator = CircuitSimulator(
    mode="netlist",
    netlist_path=netlist_path,
    node_plot_x="time",
    node_plot_y=1,
)
total_nodes = ground_truth_data.columns.size - 1  # Exclude last column
x_values_sim = simulator.steps * 1000  # Convert to ms
print("Ground Truth TIME:", ground_truth_data.index.values)
print("\nSimulation TIME:", x_values_sim)
print("\nDifference_time:", ground_truth_data.index.values - x_values_sim)
print("\n\n")
for node in range(1, total_nodes + 1):
    y_values_sim = simulator.answer[:, node - 1]  # Node 1 voltage
    # Expected values
    
    print("Ground Truth:", ground_truth_data[f"{node}"])
    print("\nSimulation:", y_values_sim)
    print("\nDifference:", ground_truth_data[f"{node}"] - y_values_sim)