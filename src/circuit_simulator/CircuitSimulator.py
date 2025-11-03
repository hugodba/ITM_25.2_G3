from typing import Literal, Optional, List
import matplotlib.pyplot as plt

from circuit_simulator import Circuit, Simulation
from circuit_simulator.elements import (
    Resistor,
    Capacitor,
    Inductor,
    VoltageSource,
    CurrentSource,
    VoltageControlledVoltageSource,
)

class CircuitSimulator:

    def __init__(
        self,
        mode: str,
        netlist_path: Optional[str] = None,
        node_plot: Literal['all'] | List[int] = 'all',
    ):
        self.netlist_path = netlist_path

        with open(self.netlist_path) as netfile:
            self.netlist = clean_netlist(netfile.readlines())

        self.ckt = Circuit(self.netlist)
        self.sim = Simulation(self.netlist)

        if mode == 'netlist':
            if netlist_path is None:
                raise ValueError("Netlist path must be provided in 'netlist' mode.")
            
        self.ckt.read_netlist()
        self.sim.read_netlist()

        if mode == 'programatic':

            # --- INSERIR AQUI A CRIAÇÃO DO CIRCUITO PROGRAMATICAMENTE ---
            self.ckt.add_element(Inductor("L3001", 1, 0, 0.001))
            self.ckt.add_element(Inductor("L3002", 2, 0, 0.00025))
            self.ckt.add_element(Inductor("L3003", 3, 0, 0.00011111111110000001))
            self.ckt.add_element(Capacitor("C2002", 1, 0, 1e-06, 1))
            self.ckt.add_element(Capacitor("C2003", 2, 0, 1e-06, 1))
            self.ckt.add_element(Capacitor("C2004", 3, 0, 1e-06, 1))
            self.ckt.add_element(VoltageControlledVoltageSource("E7000", 4, 0, 3, 0, 1))
            self.ckt.add_element(VoltageControlledVoltageSource("E7000", 5, 4, 2, 0, 1))
            self.ckt.add_element(VoltageControlledVoltageSource("E7000", 6, 5, 1, 0, 1))

            self.sim.config['analysis_type'] = ".TRAN"
            self.sim.config['time_simulation'] = 0.003
            self.sim.config['step_simulation'] = 3e-07
            self.sim.config['integration_method'] = "BE"
            self.sim.config['internal_steps'] = 1
            # --------------- FIM DA CRIAÇÃO PROGRAMÁTICA ----------------

            self.generate_netlist()

        print(f"Número de nós no circuito: {self.ckt.nodes}")
        print(self.ckt.elements)
        print(self.sim.config)

        answer, step = self.sim.time_analysis(self.ckt)
    
        
        plot_answer_vs_steps(answer, step)

    def generate_netlist(self) -> str:
        """Generate a netlist representation of the circuit."""
        # TODO: Implement netlist generation
        # get and iterate over self.ckt.elements
        # get self.sim.config
        # build file content
        # self.netlist = generated_netlist_string
        # export to self.netlist_path
        pass

    def plot(self, sim: Simulation):
        pass

def plot_answer_vs_steps(answer, steps):
    
    x_values = answer[:, 0]  # plot do nó 1 (índice 1)
    y_values = answer[:, 5]  # plot do nó 6 (índice 6)

    # Faz o gráfico
    #plt.plot(x_values, y_values, label="node1 vs node2") # plot teste chua.net
    plt.plot(steps, y_values, label="node6 vs time") # plot node x pelo tempo
    plt.xlabel("Node 1 (V)")
    plt.ylabel("Node 2 (V)")
    plt.title("Resposta no tempo")
    plt.grid(True)
    plt.show()

def clean_netlist(content: list[str]) -> list[str]:
    """Remove comentários e linhas em branco do conteúdo da netlist.

    Args:
        content (list): Conteúdo completo do arquivo de netlist em formato "readlines".

    Returns:
        list: Conteúdo limpo da netlist.
    """
    cleaned_content = []

    for line in content:
        if line[0] == "" or line[0] == "\n" or line[0] == "*":
            continue
        cleaned_content.append(line.strip("\n "))

    return cleaned_content