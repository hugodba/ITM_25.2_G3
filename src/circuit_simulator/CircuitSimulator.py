from typing import Literal
import matplotlib.pyplot as plt
import os

from circuit_simulator import Circuit, Simulation


class CircuitSimulator:
    """Class to handle circuit simulation from netlist or programatically."""

    def __init__(
        self,
        mode: str,
        netlist_path: str,
    ) -> None:
        self.mode = mode
        self.netlist_path = netlist_path
        self.netlist = []

        if mode == 'netlist':
            with open(self.netlist_path) as netfile:
                self.netlist = clean_netlist(netfile.readlines())

        self.ckt = Circuit(self.netlist)
        self.sim = Simulation(self.netlist)        

    def run(self) -> None:
        '''Run the circuit simulation.'''
        
        if self.mode == 'netlist':
            self.ckt.read_netlist()
            self.sim.read_netlist()

        elif self.mode == 'programatic':
            self.generate_netlist()

        self.answer, self.steps = self.sim.time_analysis(self.ckt)

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        results_dir = os.path.join(project_root, "results")
        os.makedirs(results_dir, exist_ok=True)
        
        file_name = os.path.basename(self.netlist_path).split(".")[0]
        out_path = os.path.join(results_dir, f"{file_name}.txt")

        with open(out_path, "w") as file:
            for answer, step in zip(self.answer, self.steps):
                answer_str = " ".join(map(str, answer))
                file.write(f"{step}, {answer_str}\n")

    def generate_netlist(self) -> None:
        """Generate a netlist representation of the circuit."""
        txt = f'{self.ckt.nodes}\n'

        elements_netlist = [element.to_netlist() for element in self.ckt.elements]
        txt += "\n".join(elements_netlist)

        txt += f'\n{self.sim.config["analysis_type"]} {self.sim.config["time_simulation"]} {self.sim.config["step_simulation"]} {self.sim.config["integration_method"]} {self.sim.config["internal_steps"]}'
        
        with open(self.netlist_path, 'w') as file:
            file.write(txt)


    def plot(
            self, 
            node_plot_x1: int | Literal['time'] = 'time',
            node_plot_y1: int | Literal['time'] = 1,
            node_plot_x2: int | Literal['time'] | None = None,
            node_plot_y2: int | Literal['time'] | None = None,
        ) -> None:
        """Plot the simulation results."""
        
        if node_plot_x1 == 'time':
            x_values = self.steps * 1000
            x_label = "Time (ms)"
        else:
            x_values = self.answer[:, node_plot_x1]
            x_label = f"Node {node_plot_x1} (V)"

        if node_plot_y1 == 'time':
            y_values = self.steps * 1000
            y_label = "Time (ms)"
        else:
            if 'mosfet' in self.netlist_path:
                y_values = self.answer[:, node_plot_y1] * 1000
                y_label = f"Id {node_plot_y1} (mA)"
            else:
                y_values = self.answer[:, node_plot_y1]
                y_label = f"Node {node_plot_y1} (V)"

         # ---- Second curve (optional) ----
        if node_plot_x2 is not None and node_plot_y2 is not None:

            plt.plot(x_values, y_values, label="Vin", color='blue')

            if node_plot_x2 == 'time':
                x2 = self.steps * 1000
            else:
                x2 = self.answer[:, node_plot_x2]

            if node_plot_y2 == 'time':
                y2 = self.steps * 1000
            else:
                y2 = self.answer[:, node_plot_y2]

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