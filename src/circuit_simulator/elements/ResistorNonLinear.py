from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class ResistorNonLinear(Element):
    """Class representing a nonlinear resistor."""
    def __init__(
        self,
        parent_circuit: "Circuit",
        name: str,
        node1: int,
        node2: int,
        v1: float,
        i1: float,
        v2: float,
        i2: float,
        v3: float,
        i3: float,
        v4: float,
        i4: float
    ) -> None:
        super().__init__(parent_circuit, name)
        self.node1 = node1 
        self.node2 = node2 
        self.v1 = v1 
        self.i1 = i1 
        self.v2 = v2
        self.i2 = i2
        self.v3 = v3
        self.i3 = i3
        self.v4 = v4
        self.i4 = i4
        
    def add_conductance(self, G, I, x_t, deltaT, method,t):
        if method == 'BE':
            vab = x_t[self.node1] - x_t[self.node2]
            
            if vab > self.v3:
                G0 = (self.i4 - self.i3) / (self.v4 - self.v3)
                I0 = self.i4 - G0 * self.v4
            
            elif vab > self.v2 and vab <= self.v3:
                G0 = (self.i3 - self.i2) / (self.v3 - self.v2)
                I0 = self.i3 - G0 * self.v3
            
            else:
                G0 = (self.i2 - self.i1) / (self.v2 - self.v1)
                I0 = self.i2 - G0 * self.v2
            
            
            G[self.node1,self.node1] += G0
            G[self.node1,self.node2] += - G0
            G[self.node2,self.node1] += - G0
            G[self.node2,self.node2] += G0

            I[self.node1] += -I0
            I[self.node2] += I0      

            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented ResistorNonLinear yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented ResistorNonLinear yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")