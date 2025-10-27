from src.circuit_simulator.Element import Element

class Indutor(Element):
    """Class representing an inductor."""
    def __init__(self, name: str, node1: int, node2: int, inductance: float,
                  initial_current: float = 0.0, extra_line: int = None):
        super().__init__(name)
        self.node1 = node1 -1  # First node of the inductor
        self.node2 = node2 -1  # Second node of the inductor
        self.inductance = inductance  # Inductance value in Henrys
        self.initial_current = initial_current  # Initial current through the inductor
        self.extra_line = extra_line  # Extra line for inductor modeling

    def add_conductance(self, G, I, deltaT):
        
        if self.node1 >= 0:
            G[self.node1,self.extra_line] += 1
            G[self.extra_line,self.node1] += -1
        if self.node2 >= 0:
            G[self.node2,self.extra_line] += -1
            G[self.extra_line,self.node2] += 1
        
        
        G[self.extra_line,self.extra_line] += self.inductance/deltaT
        I[self.extra_line] += (self.inductance/deltaT) * self.initial_current

        return G, I
    
    def update(self, x_t):
        self.initial_current = x_t[self.extra_line]
        # Specific implementation for inductor to add its contribution to the conductance matrix (G) and current vector (I)
    