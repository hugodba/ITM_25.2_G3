from src.circuit_simulator.Element import Element

class Resistor(Element):
    """Class representing a resistor."""
    def __init__(self, name: str, node1: int, node2: int, resistance: float):
        super().__init__(name)
        self.node1 = node1 -1 # First node of the resistor
        self.node2 = node2 -1 # Second node of the resistor
        self.resistance = resistance  # Resistance value in Ohms

    def add_conductance(self, G, I, deltaT):
        # Specific implementation for resistor to add its contribution to the conductance matrix (G) and current vector (I)

        if self.node1 >= 0:
            G[self.node1,self.node1] += 1/self.resistance

        if self.node1 >= 0 and self.node2 >= 0:
            G[self.node1,self.node2] += - 1/self.resistance
            G[self.node2,self.node1] += - 1/self.resistance

        if self.node2 >= 0:
            G[self.node2,self.node2] += 1/self.resistance
        
        return G, I
    
