from typing import Literal
import matplotlib.pyplot as plt

from circuit_simulator import Circuit, Simulation
from circuit_simulator.elements import (
    Resistor,
    Capacitor,
    Inductor,
    VoltageSINSource,
    VoltageDCSource,
    VoltagePulseSource,
    ResistorNonLinear,
    CurrentDCSource,
    CurrentSINSource,
    CurrentPulseSource,
    VoltageControlledVoltageSource,
    VoltageControlledCurrentSource,
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    OperationalAmplifier,
    Diode
)

class CircuitSimulator:

    def __init__(
        self,
        mode: str,
        netlist_path: str,
        node_plot_x1: int | Literal['time'] = 'time',
        node_plot_y1: int | Literal['time'] = 1,
        node_plot_x2: int | Literal['time'] | None = None,
        node_plot_y2: int | Literal['time'] | None = None,
    ):
        self.netlist_path = netlist_path
        self.node_plot_x1 = node_plot_x1
        self.node_plot_y1 = node_plot_y1

        self.node_plot_x2 = node_plot_x2
        self.node_plot_y2 = node_plot_y2

        if mode == 'programatic':
            with open(self.netlist_path, 'w', encoding='utf-8') as netfile:
                pass

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
            self.ckt.nodes = 6

            self.ckt.add_element(Inductor(self.ckt, "L3001", 1, 0, 0.001))
            self.ckt.add_element(Inductor(self.ckt, "L3002", 2, 0, 0.00025))
            self.ckt.add_element(Inductor(self.ckt, "L3003", 3, 0, 0.00011111111110000001))
            self.ckt.add_element(Capacitor(self.ckt, "C2002", 1, 0, 1e-06, 1))
            self.ckt.add_element(Capacitor(self.ckt, "C2003", 2, 0, 1e-06, 1))
            self.ckt.add_element(Capacitor(self.ckt, "C2004", 3, 0, 1e-06, 1))
            self.ckt.add_element(VoltageControlledVoltageSource(self.ckt, "E7000", 4, 0, 3, 0, 1))
            self.ckt.add_element(VoltageControlledVoltageSource(self.ckt, "E7001", 5, 4, 2, 0, 1))
            self.ckt.add_element(VoltageControlledVoltageSource(self.ckt, "E7002", 6, 5, 1, 0, 1))

            self.sim.config['analysis_type'] = ".TRAN"
            self.sim.config['time_simulation'] = 0.003
            self.sim.config['step_simulation'] = 3e-07
            self.sim.config['integration_method'] = "BE"
            self.sim.config['internal_steps'] = 1
            # --------------- FIM DA CRIAÇÃO PROGRAMÁTICA ----------------

            self.generate_netlist()

        self.answer, self.steps = self.sim.time_analysis(self.ckt)

        self.plot()

    
        
    def generate_netlist(self) -> str:
        """Generate a netlist representation of the circuit."""
        # TODO: Implement netlist generation
        # get and iterate over self.ckt.elements

        for element in self.ckt.elements:
            pass
        # get self.sim.config
        # build file content
        # self.netlist = generated_netlist_string
        # export to self.netlist_path
        pass

    def plot(self):

        if self.node_plot_x1 == 'time':
            x_values = self.steps * 1000
            x_label = "Time (ms)"
        else:
            x_values = self.answer[:, self.node_plot_x1 - 1]
            x_label = f"Node {self.node_plot_x1} (V)"

        if self.node_plot_y1 == 'time':
            y_values = self.steps * 1000
            y_label = "Time (ms)"
        else:
            y_values = self.answer[:, self.node_plot_y1 - 1]
            y_label = f"Node {self.node_plot_y1} (V)"

        


         # ---- Second curve (optional) ----
        if self.node_plot_x2 is not None and self.node_plot_y2 is not None:

            plt.plot(x_values, y_values, label="Vin", color='blue')

            if self.node_plot_x2 == 'time':
                x2 = self.steps * 1000
            else:
                x2 = self.answer[:, self.node_plot_x2 - 1]

            if self.node_plot_y2 == 'time':
                y2 = self.steps * 1000
            else:
                y2 = self.answer[:, self.node_plot_y2 - 1]

            plt.plot(x2, y2, label="Vout", color='red')
            plt.legend()
            #plt.legend(loc="upper right")


        plt.plot(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
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