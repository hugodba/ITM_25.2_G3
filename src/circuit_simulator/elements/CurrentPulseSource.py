from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element
import numpy as np

class CurrentPulseSource(Element):
    """Class representing a voltage pulse source."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        source_type: str,
        current_amplitude_one: float,
        current_amplitude_two: float,
        signal_delay: float,
        rise_time: float,
        fall_time: float,
        pulse_time: float,
        signal_period: float,
        cycle_number: float,

    ) -> None:
        super().__init__(name)
        self.node1 = node1  
        self.node2 = node2
        self.source_type = source_type
        self.current_amplitude_one = current_amplitude_one
        self.current_amplitude_two = current_amplitude_two
        self.signal_delay = signal_delay
        self.rise_time = rise_time
        self.fall_time = fall_time
        self.pulse_time = pulse_time
        self.signal_period = signal_period
        self.cycle_number = cycle_number
        

    def actual_current_value(self, actual_time):
        if actual_time < self.signal_delay:
            return self.current_amplitude_one
        
        real_time = actual_time - self.signal_delay
        k = int(real_time // self.signal_period)
        tau = real_time % self.signal_period

        if self.cycle_number > 0 and k >= self.cycle_number:
            return self.current_amplitude_one
        
        if tau < self.rise_time:
            return self.current_amplitude_one + (self.current_amplitude_two - self.current_amplitude_one) * (tau / self.rise_time)
        elif tau < self.pulse_time + self.rise_time:
            return self.current_amplitude_two
        elif tau < self.pulse_time + self.rise_time + self.fall_time:
            return self.current_amplitude_two + (self.current_amplitude_one - self.current_amplitude_two) * ((tau - (self.pulse_time + self.rise_time)) / self.fall_time)
        else:
            return self.current_amplitude_one
        
        
    def add_conductance(self, G, I, x_t, deltaT, method,t):

        if method == 'BE':
            
            i_t = self.actual_current_value(t)

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
        return f"{self.name} {self.node1} {self.node2} {self.source_type} {self.current_amplitude_one} {self.current_amplitude_two} {self.signal_delay} {self.rise_time} {self.fall_time} {self.pulse_time} {self.signal_period} {self.cycle_number}"