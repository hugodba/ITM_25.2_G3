from typing import Literal, Optional, List
import matplotlib.pyplot as plt

from circuit_simulator import Circuit, Simulation
from circuit_simulator.elements import Resistor


def main(
    mode: Literal['netlist', 'programatic'],
    netlist_path: Optional[str] = None,
    node_plot: Literal['all'] | List[int] = 'all',
    export_netlist: bool = False,
):
    ckt = Circuit(netlist_path)

    if mode == 'netlist':
        if netlist_path is None:
            raise ValueError("Netlist path must be provided in 'netlist' mode.")
        
    print(f"Lendo arquivo netlist em: {netlist_path}")


    if mode == 'programatic':
        # exemplo de criação programática de circuito
        ckt.add_element(Resistor("R1", 1, 0, 1000))
        ckt.add_element(Resistor("R2", 2, 0, 2000))

        ckt.generate_netlist()
        
        if export_netlist:
            if netlist_path is None:
                raise ValueError("Netlist path must be provided to export netlist.")
            
            ckt.export_netlist()

    simulation = Simulation()
    try:
        answer, step = simulation.time_analysis(ckt)
    except ValueError as e:
        print(f"Erro durante a simulação: {e}")
        return
    
    plot_answer_vs_steps(answer, step)

def plot_answer_vs_steps(answer, steps):

    x_values = answer[:, 0]  # plot do nó 1 (índice 1)
    y_values = answer[:, 0]  # plot do nó 6 (índice 6)

    # Faz o gráfico
    #plt.plot(x_values, y_values, label="node1 vs node2") # plot teste chua.net
    plt.plot(steps, y_values, label="node6 vs time") # plot node x pelo tempo
    plt.xlabel("Node 1 (V)")
    plt.ylabel("Node 2 (V)")
    plt.title("Resposta no tempo")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main(
        mode='netlist',
        netlist_path=r'C:\Users\hugob\Documents\ITM_25.2_G3\netlists\examples\pulse.net',
        node_plot=5,
        export_netlist=True
    )
