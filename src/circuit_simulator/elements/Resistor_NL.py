from src.circuit_simulator.Element import Element

class Resistor_nl(Element):
    """Class representing a nonlinear resistor."""
    def __init__(self, name: str, node1: int, node2: int, v1: float, i1: float, v2: float, i2: float,
                 v3: float, i3: float, v4: float, i4: float):
        
        super().__init__(name)
        self.node1 = node1  # First node of the nonlinear resistor
        self.node2 = node2  # Second node of the nonlinear resistor
        self.v1 = v1  # Resistance value in one state
        self.i1 = i1  # Resistance value in another state
        self.v2 = v2
        self.i2 = i2
        self.v3 = v3
        self.i3 = i3
        self.v4 = v4
        self.i4 = i4
        

    def add_conductance(self, G, I, method='backward_euler'):
        # Specific implementation for nonlinear resistor to add its contribution to the conductance matrix (G) and current vector (I)
        pass