from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class CurrentControlledVoltageSource(Element):
    """Class representing a VoltageControlledVoltageSource element."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        control_node1: int,
        control_node2: int,
        gain: float,

    ) -> None:
        super().__init__(name)
        self.node1 = node1
        self.node2 = node2
        self.control_node1 = control_node1
        self.control_node2 = control_node2
        self.gain = gain

    def on_add(self):
        self.extra_line = self.parent_circuit.nodes + self.parent_circuit.extra_lines + 2
        self.parent_circuit.extra_lines += 2

    def add_conductance(self, G, I, x_t, deltaT, method, t):
        if method == 'BE':
            G[self.node1,self.extra_line] = 1
            G[self.node2,self.extra_line] = -1
            G[self.control_node1,self.extra_line + 1] = 1
            G[self.control_node2,self.extra_line + 1] = -1
            
            G[self.extra_line,self.control_node1] = -1
            G[self.extra_line,self.control_node2] = 1
            G[self.extra_line + 1,self.control_node1] = -1
            G[self.extra_line + 1,self.control_node2] = 1

            G[self.extra_line + 1, self.extra_line + 1] = self.gain
            
            return G,I
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageControlledVoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")