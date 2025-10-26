from src.circuit_simulator.Element import Element

class Resistor(Element):
    """Class representing a resistor."""
    def __init__(self, name: str, node1: int, node2: int, resistance: float):
        super().__init__(name)
        self.node1 = node1  # First node of the resistor
        self.node2 = node2  # Second node of the resistor
        self.resistance = resistance  # Resistance value in Ohms

    def add_conductance(self, G, I, method='backward_euler'):
        # Specific implementation for resistor to add its contribution to the conductance matrix (G) and current vector (I)
        pass
