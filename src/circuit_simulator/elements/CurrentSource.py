from Element import Element

class CurrentSource(Element):
    """Class representing a current source."""
    def __init__(self, name: str, node1: int, node2: int, current: float):
        super().__init__(name)
        self.node1 = node1  # Positive terminal node
        self.node2 = node2  # Negative terminal node
        self.current = current  # Current value in Amperes

    def add_stamp_backward(self):
        # Specific implementation for current source to add its contribution to the conductance matrix (G) and current vector (I)
        pass

    def __str__(self):
        return f"Name: {self.name},"\
               f"Component: Resistor,"\
               f"Value: {self.R} Ω,"\
               f"Node a: {self.nodeA},"\
               f"Node b: {self.nodeB}"