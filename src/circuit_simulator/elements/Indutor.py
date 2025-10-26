from src.circuit_simulator.Element import Element

class Indutor(Element):
    """Class representing an inductor."""
    def __init__(self, name: str, node1: int, node2: int, inductance: float, initial_current: float = 0.0):
        super().__init__(name)
        self.node1 = node1  # First node of the inductor
        self.node2 = node2  # Second node of the inductor
        self.inductance = inductance  # Inductance value in Henrys
        self.initial_current = initial_current  # Initial current through the inductor

    def add_conductance(self, G, I, method='backward_euler'):
        # Specific implementation for inductor to add its contribution to the conductance matrix (G) and current vector (I)
        pass