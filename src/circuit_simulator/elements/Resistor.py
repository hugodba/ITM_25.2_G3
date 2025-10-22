from src.circuit_simulator.Element import Element
from numpy import ndarray


class Resistor(Element, prefix='r'):
    """Class representing a Resistor."""

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, method: str
        ):

        super().__init__(splitline_netlist, Yn, In, method)
        self.elem_type = "invariant"
        self.nodeA = splitline_netlist[1]
        self.nodeB = splitline_netlist[2]
        self.R = splitline_netlist[3]
        self.add_stamp(method)
        #return Yn, In  <- doesn't need, it changes by reference.

    def add_stamp_backward(self):
        g = 1/self.R
        self.Yn[self.nodeA, self.nodeA] += g
        self.Yn[self.nodeB, self.nodeB] += g
        self.Yn[self.nodeA, self.nodeB] += -g
        self.Yn[self.nodeB, self.nodeA] += -g

    def __str__(self):
        return f"Name: {self.name},"\
               f"Component: Resistor,"\
               f"Value: {self.R} Ω,"\
               f"Node a: {self.nodeA},"\
               f"Node b: {self.nodeB}"