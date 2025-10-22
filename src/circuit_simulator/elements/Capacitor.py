from src.circuit_simulator.Element import Element
from numpy import ndarray


class Capacitor(Element, prefix='c'):
    """Class representing a Capacitor."""

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, method: str, 
            deltaT: float, e0: ndarray
        ):
        super().__init__(splitline_netlist, Yn, In, method)
        self.elem_type = "variant"
        self.nodeA = splitline_netlist[1]
        self.nodeB = splitline_netlist[2]
        self.C = splitline_netlist[3]
        self.v_initial = splitline_netlist[4]
        self.deltaT = deltaT
        self.e0 = e0
        self.add_stamp(method)
        #return Yn, In  <- doesn't need, it changes by reference.


    def add_stamp_backward(self):
        # Add capacitor current as variable of matrix equation (add 1 line to Yn and In)
        self.add_newblanklines_YnIn(newlines=1)

        # Add Yn stamp
        self.Yn[self.nodeA, self.nodeA] +=  self.C/self.deltaT
        self.Yn[self.nodeA, self.nodeB] +=  -self.C/self.deltaT
        self.Yn[self.nodeB, self.nodeA] +=  -self.C/self.deltaT
        self.Yn[self.nodeB, self.nodeB] +=  self.C/self.deltaT

        # Get v(t-deltaT)
        eA = eB = 0
        if self.nodeA != 0:
            eA = self.e0[self.nodeA - 1]
        if self.nodeB != 0:
            eB = self.e0[self.nodeB - 1]

        v0 = self.v_initial
        if len(self.e0) != 0: # Se não for o primeiro passo de tempo.
            v0 = eA - eB      # Tensão no capacitor no tempo anterior
            
        # Add In Stamp
        self.In[self.nodeA] += v0*self.C/self.deltaT 
        self.In[self.nodeB] += -v0*self.C/self.deltaT 


    def __str__(self):
        return f"Name: {self.name},"\
               f"Component: Capacitor,"\
               f"Value: {self.C} F,"\
               f"Node a: {self.nodeA},"\
               f"Node b: {self.nodeB},"\
               f"Delta T: {self.deltaT} s"