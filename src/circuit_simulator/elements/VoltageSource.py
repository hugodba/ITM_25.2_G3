from circuit_simulator import Element

class VoltageSource(Element):
    """Class representing a voltage source."""
    def __init__(self, name: str, node1: int, node2: int, source_type: str, voltage: float, extra_line: int = None):
        super().__init__(name)
        self.node1 = node1  
        self.node2 = node2
        self.source_type = source_type
        self.voltage = voltage
        self.extra_line = extra_line

    def add_conductance(self, G, I, x_t, deltaT, method):
        
        if method == 'BE':
            G[self.node1,self.extra_line] += 1
            G[self.node2,self.extra_line] += -1
            G[self.extra_line,self.node1] += -1
            G[self.extra_line,self.node2] += 1

            I[self.extra_line] += -self.voltage
            
            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")