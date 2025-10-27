from circuit_simulator import Element

class FTCT(Element):
    """Class representing a FTCT element."""
    def __init__(self, name: str, node1: int, node2: int, control_node1: float, controle_node2: float, gain: float, extra_line: int = None):
        super().__init__(name)
        self.node1 = node1 -1 # First node of the FTCT
        self.node2 = node2 -1 # Second node of the FTCT
        self.control_node1 = control_node1 -1 # Some parameter specific to FTCT
        self.control_node2 = controle_node2 -1 # Another parameter specific to FTCT
        self.gain = gain  # Gain of the FTCT
        self.extra_line = extra_line  # Extra line for FTCT modeling

    def add_conductance(self, G, I, x_t, deltaT):
        # Specific implementation for FTCT to add its contribution to the conductance matrix (G) and current vector (I)

        if self.node1 >= 0:
            G[self.node1,self.extra_line] += 1
            G[self.extra_line,self.node1] += -1
        if self.node2 >= 0:
            G[self.node2,self.extra_line] +=  -1
            G[self.extra_line,self.node2] += +1
        if self.control_node1 >= 0:
            G[self.extra_line,self.control_node1] += self.gain
        if self.control_node2 >= 0:
            G[self.extra_line,self.control_node2] += -self.gain
            
        return G, I