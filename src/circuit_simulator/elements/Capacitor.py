from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class Capacitor(Element):
    """Class representing a capacitor."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        capacitance: float,
        initial_voltage: float = 0.0
    ) -> None:
        super().__init__(name)
        self.node1 = node1  
        self.node2 = node2  
        self.capacitance = capacitance  
        self.initial_voltage = initial_voltage 
        

    def add_conductance(self, G, I, x_t, deltaT, method, t):
        
        if method == 'BE':
            
            G[self.node1,self.node1] += self.capacitance/deltaT
            G[self.node1,self.node2] += - self.capacitance/deltaT
            G[self.node2,self.node1] += - self.capacitance/deltaT
            G[self.node2,self.node2] += self.capacitance/deltaT

            I[self.node1] += (self.capacitance/deltaT) * self.initial_voltage
            I[self.node2] += (-self.capacitance/deltaT) * self.initial_voltage
            
            return G, I
        elif method == 'FE':
            print("Forward Euler method not implemented Capacitor yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented Capacitor yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")
    

    def update(self, x_t):
        self.initial_voltage = x_t[self.node1] - x_t[self.node2]

    def to_netlist(self):
        return f"{self.name} {self.node1} {self.node2} {self.capacitance} IC={self.initial_voltage}"
