from circuit_simulator import Element

class CurrentSource(Element):
    """Class representing a current source."""
    def __init__(self, name: str, node1: int, node2: int, source_type: str, current: float):
        super().__init__(name)
        self.node1 = node1  
        self.node2 = node2
        self.source_type = source_type
        self.current = current  

    def add_conductance(self, G, I, x_t, deltaT, method):
        
        if method == 'BE':
            I[self.node1] += -self.current
            I[self.node2] += self.current

            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented CurrentSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented CurrentSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")
