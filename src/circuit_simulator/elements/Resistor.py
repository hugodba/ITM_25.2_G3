from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class Resistor(Element):
    """Class representing a resistor."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        resistance: float
    ) -> None:
        super().__init__(name)
        self.node1 = node1
        self.node2 = node2
        self.resistance = resistance  

    def add_conductance(self, G, I, x_t, deltaT, method,t):
        
        if method == 'BE':
            
            G[self.node1,self.node1] += 1/self.resistance
            G[self.node1,self.node2] += - 1/self.resistance
            G[self.node2,self.node1] += - 1/self.resistance
            G[self.node2,self.node2] += 1/self.resistance
            
            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented Resistor yet.")
            return G, I
        
        elif method == 'TRAP':
            print("Trapezoidal method not implemented Resistor yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")
        
    
