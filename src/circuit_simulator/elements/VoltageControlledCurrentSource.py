from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class VoltageControlledCurrentSource(Element):
    """Class representing a current controlled current source."""
    def __init__(
        self,
        parent_circuit: "Circuit",
        name: str,
        node1: int,
        node2: int,
        control_node1: int,
        control_node2: int,
        gain: float,

    ) -> None:
        super().__init__(parent_circuit, name)
        self.node1 = node1 
        self.node2 = node2
        self.control_node1 = control_node1
        self.control_node2 = control_node2
        self.gain = gain

    def add_conductance(self, G, I, x_t, deltaT, method, t):
        if method == 'BE':
            G[self.node1,self.control_node1] = self.gain
            G[self.node1,self.control_node2] = -self.gain
            G[self.node2,self.control_node1] = -self.gain
            G[self.node2,self.control_node2] = self.gain
                    
            return G,I
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")