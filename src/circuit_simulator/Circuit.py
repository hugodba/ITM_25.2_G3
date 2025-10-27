from Simulation_config import Simulationconfig
from src.circuit_simulator.elements.Resistor_NL import Resistor_nl

class Circuit:
    """Base class for circuits."""
    def __init__(self, nodes: int):
        self.elements = []
        self.config = None
        self.nodes = nodes
        self.extra_lines = 0

    def add_element(self, element):
        self.elements.append(element)

    def is_nonlinear(self):
        for element in self.elements:
            if isinstance(element, Resistor_nl):
                return True
        return False
    
    def set_config(self, sim_config: Simulationconfig):
        self.config = sim_config
        print(f"Configuração de simulação definida: {sim_config}")

    def update(self, x_t):
        for element in self.elements:
            element.update(x_t)

    def __str__(self):
        return f"Circuit with {len(self.elements)} elements."
