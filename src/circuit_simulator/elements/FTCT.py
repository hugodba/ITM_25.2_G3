from src.circuit_simulator.Element import Element

class FTCT(Element):
    """Class representing a FTCT element."""
    def __init__(self, name: str, node1: int, node2: int, control_node1: float, controle_node2: float, gain: float):
        super().__init__(name)
        self.node1 = node1  # First node of the FTCT
        self.node2 = node2  # Second node of the FTCT
        self.param1 = control_node1  # Some parameter specific to FTCT
        self.param2 = controle_node2  # Another parameter specific to FTCT
        self.gain = gain  # Gain of the FTCT

    def add_conductance(self, G, I, method='backward_euler'):
        # Specific implementation for FTCT to add its contribution to the conductance matrix (G) and current vector (I)
        pass