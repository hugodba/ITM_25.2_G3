from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element
import numpy as np

class CurrentSINSource(Element):
    """Class representing a voltage source."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        source_type: str,
        current: float,
        signal_amplitude: float,
        signal_frequency: float,
        signal_delay: float,
        signal_damping: float,
        signal_phase: float,
        cycle_number: int,
    ) -> None:
        super().__init__(name)
        self.node1 = node1
        self.node2 = node2
        self.source_type = source_type
        self.signal_amplitude = signal_amplitude
        self.signal_frequency = signal_frequency
        self.signal_delay = signal_delay
        self.signal_damping = signal_damping
        self.signal_phase = signal_phase
        self.cycle_number = cycle_number
        
        self.current = current

    def add_conductance(self, G, I, x_t, deltaT, method,t):

        if method == 'BE':

            if t < self.signal_delay or t > self.cycle_number:
                i_t = self.current + self.signal_amplitude * np.sin((np.pi / 180) * self.signal_phase)
            else:
                i_t = self.current + self.signal_amplitude * np.exp(-self.signal_damping * (t - self.signal_delay)) * np.sin(2 * np.pi * self.signal_frequency * (t - self.signal_delay) + ((np.pi/180) * self.signal_phase))
            
            I[self.node1] += -i_t
            I[self.node2] += i_t

            return G, I
            
        
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")
        
    def to_netlist(self):
        return f"{self.name} {self.node1} {self.node2} {self.source_type} {self.current} {self.signal_amplitude} {self.signal_frequency} {self.signal_delay} {self.signal_damping} {self.signal_phase} {self.cycle_number}"