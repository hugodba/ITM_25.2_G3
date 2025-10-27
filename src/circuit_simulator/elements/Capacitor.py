from src.circuit_simulator.Element import Element

class Capacitor(Element):
    """Class representing a capacitor."""
    def __init__(self, name: str, node1: int, node2: int, capacitance: float, initial_voltage: float = 0.0):
        super().__init__(name)
        self.node1 = node1 -1 # First node of the capacitor
        self.node2 = node2 -1 # Second node of the capacitor
        self.capacitance = capacitance  # Capacitance value in Farads
        self.initial_voltage = initial_voltage  # Initial voltage across the capacitor
        

    def add_conductance(self, G, I, deltaT):

        if self.node1 >= 0:
            G[self.node1,self.node1] += self.capacitance/deltaT
            I[self.node1] += (self.capacitance/deltaT) * self.initial_voltage

        if self.node1 >= 0 and self.node2 >= 0:
            G[self.node1,self.node2] += - self.capacitance/deltaT
            G[self.node2,self.node1] += - self.capacitance/deltaT

        if self.node2 >= 0:
            G[self.node2,self.node2] += self.capacitance/deltaT
            I[self.node2] += (-self.capacitance/deltaT) * self.initial_voltage
        
        return G, I
    
    def update(self, x_t):
        if self.node2 >= 0:
            self.initial_voltage = x_t[self.node2]
        elif self.node1 >= 0:
            self.initial_voltage = x_t[self.node1]
        elif self.node1 >= 0 and self.node2 >= 0:
            self.initial_voltage = x_t[self.node1] - x_t[self.node2]
        else:
            self.initial_voltage = 0.0

    
        # Specific implementation for capacitor to add its contribution to the conductance matrix (G) and current vector (I)