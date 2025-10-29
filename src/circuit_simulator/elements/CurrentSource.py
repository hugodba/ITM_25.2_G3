from circuit_simulator import Element

class CurrentSource(Element):
    """Class representing a current source."""
    def __init__(self, name: str, node1: int, node2: int, current: float):
        super().__init__(name)
        self.node1 = node1  
        self.node2 = node2  
        self.current = current  

    def add_conductance(self, G, I, x_t, deltaT, method):
        
        pass
