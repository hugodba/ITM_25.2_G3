from circuit_simulator import Element

class ResistorNL(Element):
    """Class representing a nonlinear resistor."""
    def __init__(self, name: str, node1: int, node2: int, v1: float, i1: float, v2: float, i2: float,
                 v3: float, i3: float, v4: float, i4: float):
        
        super().__init__(name)
        self.node1 = node1 -1 # First node of the nonlinear resistor
        self.node2 = node2 -1 # Second node of the nonlinear resistor
        self.v1 = v1  # Resistance value in one state
        self.i1 = i1  # Resistance value in another state
        self.v2 = v2
        self.i2 = i2
        self.v3 = v3
        self.i3 = i3
        self.v4 = v4
        self.i4 = i4
        
    def add_conductance(self, G, I, x_t, deltaT):
        vab = 0.0
        if self.node1 >= 0:
            vab += x_t[self.node1]
        if self.node2 >= 0:
            vab -= x_t[self.node2]
        
        if vab > self.v3:
            G0 = (self.i4 - self.i3) / (self.v4 - self.v3)
            I0 = self.i4 - G0 * self.v4
        
        elif vab > self.v2 and vab <= self.v3:
            G0 = (self.i3 - self.i2) / (self.v3 - self.v2)
            I0 = self.i3 - G0 * self.v3
        
        else:
            G0 = (self.i2 - self.i1) / (self.v2 - self.v1)
            I0 = self.i2 - G0 * self.v2
        
        if self.node1 >= 0:
            G[self.node1,self.node1] += G0
            I[self.node1] += -I0

        if self.node1 >= 0 and self.node2 >= 0:
            G[self.node1,self.node2] += - G0
            G[self.node2,self.node1] += - G0
        if self.node2 >= 0:
            G[self.node2,self.node2] += G0
            I[self.node2] += I0      

        return G, I

    