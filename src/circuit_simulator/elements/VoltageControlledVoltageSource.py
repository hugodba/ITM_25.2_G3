from circuit_simulator import Element

class VoltageControlledVoltageSource(Element):
    """Class representing a VoltageControlledVoltageSource element."""
    def __init__(self, name: str, node1: int, node2: int, control_node1: float, controle_node2: float, gain: float, extra_line: int = None):
        super().__init__(name)
        self.node1 = node1 
        self.node2 = node2
        self.control_node1 = control_node1
        self.control_node2 = controle_node2
        self.gain = gain 
        self.extra_line = extra_line

    def add_conductance(self, G, I, x_t, deltaT, method):
        if method == 'BE':

            G[self.node1,self.extra_line] += 1
            G[self.extra_line,self.node1] += -1
            G[self.node2,self.extra_line] +=  -1
            G[self.extra_line,self.node2] += +1
            
            G[self.extra_line,self.control_node1] += self.gain
            G[self.extra_line,self.control_node2] += -self.gain
                
            return G, I
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")