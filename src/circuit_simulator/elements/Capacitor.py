from src.circuit_simulator.Element import Element

class Capacitor(Element):
    """Class representing a capacitor."""
    def __init__(self, name: str, node1: int, node2: int, capacitance: float, initial_voltage: float = 0.0):
        super().__init__(name)
        self.node1 = node1  # First node of the capacitor
        self.node2 = node2  # Second node of the capacitor
        self.capacitance = capacitance  # Capacitance value in Farads
        self.initial_voltage = initial_voltage  # Initial voltage across the capacitor
        

    def add_conductance(self, G, I, method='backward_euler'):
        # Specific implementation for capacitor to add its contribution to the conductance matrix (G) and current vector (I)
        pass