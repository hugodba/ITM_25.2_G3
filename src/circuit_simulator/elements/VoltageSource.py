from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element
import numpy as np

class VoltageSource(Element):
    """Class representing a voltage source."""
    def __init__(
        self,
        parent_circuit: "Circuit",
        name: str,
        node1: int,
        node2: int,
        source_type: str,
        voltage: float,
        signal_amplitude: None,
        signal_frequency: None,
        signal_delay: None,
        signal_damping: None,
        signal_phase: None,
        cycle_number: None
    ) -> None:
        super().__init__(parent_circuit, name)
        self.node1 = node1  
        self.node2 = node2
        self.source_type = source_type
        try: 
            if self.source_type == "SIN":
                self.signal_amplitude = signal_amplitude
                self.signal_frequency = signal_frequency
                self.signal_delay = signal_delay
                self.signal_damping = signal_damping
                self.signal_phase = signal_phase
                self.cycle_number = cycle_number
        except Exception as e:
            pass
        
        
        self.voltage = voltage
        self.extra_line = parent_circuit.nodes + parent_circuit.extra_lines + 1

        self.parent_circuit.extra_lines += 1

    def add_conductance(self, G, I, x_t, deltaT, method,t):

        if method == 'BE':
            if self.source_type == "DC":
                G[self.node1,self.extra_line] += 1
                G[self.node2,self.extra_line] += -1
                G[self.extra_line,self.node1] += -1
                G[self.extra_line,self.node2] += 1

                I[self.extra_line] += -self.voltage
                
                return G, I
            elif self.source_type == "SIN":
                
                G[self.node1,self.extra_line] += 1
                G[self.node2,self.extra_line] += -1
                G[self.extra_line,self.node1] += -1
                G[self.extra_line,self.node2] += 1


                if t < self.signal_delay or t > self.cycle_number:
                    v_t = self.voltage + self.signal_amplitude * np.sin((np.pi / 180) * self.signal_phase)
                else:
                    v_t = self.voltage + self.signal_amplitude * np.exp(-self.signal_damping * (t - self.signal_delay)) * np.sin(2 * np.pi * self.signal_frequency * (t - self.signal_delay) + ((np.pi/180) * self.signal_phase))
                
                I[self.extra_line] += -v_t


                return G, I
            else:
                print(f"Source type {self.source_type} not implemented")
                return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented VoltageSource yet.")
            return G, I
        elif method == 'TRAP':
            print("Trapezoidal method not implemented VoltageSource yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")