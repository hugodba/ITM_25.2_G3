from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element
import numpy as np

class VoltagePulseSource(Element):
    """Class representing a voltage pulse source."""
    def __init__(
        self,
        name: str,
        node1: int,
        node2: int,
        source_type: str,
        voltage_amplitude_one: float,
        voltage_amplitude_two: float,
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
        self.voltage_amplitude_one = voltage_amplitude_one
        self.voltage_amplitude_two = voltage_amplitude_two
        self.signal_delay = signal_delay
        self.rise_time = rise_time
        self.fall_time = fall_time
        self.pulse_time = pulse_time
        self.signal_period = signal_period
        self.cycle_number = cycle_number

    def on_add(self):
        self.extra_line = self.parent_circuit.nodes + self.parent_circuit.extra_lines + 1
        self.parent_circuit.extra_lines += 1

    def actual_voltage_value(self, actual_time):
        if actual_time < self.signal_delay:
            return self.voltage_amplitude_one
        
        real_time = actual_time - self.signal_delay
        k = int(real_time // self.signal_period)
        tau = real_time % self.signal_period

        if self.cycle_number > 0 and k >= self.cycle_number:
            return self.voltage_amplitude_one
        
        if tau < self.rise_time:
            return self.voltage_amplitude_one + (self.voltage_amplitude_two - self.voltage_amplitude_one) * (tau / self.rise_time)
        elif tau < self.pulse_time + self.rise_time:
            return self.voltage_amplitude_two
        elif tau < self.pulse_time + self.rise_time + self.fall_time:
            return self.voltage_amplitude_two + (self.voltage_amplitude_one - self.voltage_amplitude_two) * ((tau - (self.pulse_time + self.rise_time)) / self.fall_time)
        else:
            return self.voltage_amplitude_one
        
        
    def add_conductance(self, G, I, x_t, deltaT, method,t):

        if method == 'BE':
            
            G[self.node1,self.extra_line] = 1
            G[self.node2,self.extra_line] = -1
            G[self.extra_line,self.node1] = -1
            G[self.extra_line,self.node2] = 1

            v_t = self.actual_voltage_value(t)
            I[self.extra_line] = -v_t

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
        return f"{self.name} {self.node1} {self.node2} {self.source_type} {self.voltage_amplitude_one} {self.voltage_amplitude_two} {self.signal_delay} {self.rise_time} {self.fall_time} {self.pulse_time} {self.signal_period} {self.cycle_number}"