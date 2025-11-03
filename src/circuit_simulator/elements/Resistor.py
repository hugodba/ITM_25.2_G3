<<<<<<< HEAD
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class Resistor(Element):
    """Class representing a resistor."""
    def __init__(
        self,
        parent_circuit: "Circuit",
        name: str,
        node1: int,
        node2: int,
        resistance: float
    ) -> None:
        super().__init__(parent_circuit, name)
        self.node1 = node1
        self.node2 = node2
        self.resistance = resistance  

    def add_conductance(self, G, I, x_t, deltaT, method):
        
        if method == 'BE':
            
            G[self.node1,self.node1] += 1/self.resistance
            G[self.node1,self.node2] += - 1/self.resistance
            G[self.node2,self.node1] += - 1/self.resistance
            G[self.node2,self.node2] += 1/self.resistance
            
            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented Resistor yet.")
            return G, I
        
        elif method == 'TRAP':
            print("Trapezoidal method not implemented Resistor yet.")
            return G, I
        else:
            raise ValueError("Método de análise desconhecido.")
        
    
=======
from src.circuit_simulator.Element import Element
from numpy import ndarray


class Resistor(Element, prefix='r'):
    """Classe representando um Resistor."""

    elem_type = "invariant"
    elem_name = "Resistor"

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, elems_info: dict, method: str, **kwargs
        ):

        super().__init__(splitline_netlist, Yn, In, elems_info, method)
        self.extract_values(splitline_netlist)
        self.add_stamp(method)
        self.save_info()

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "Valor": self.R,
                "Unidade": "Ω",
            }

    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            self.R = float(splitline_netlist[3])
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do resistor "
                             f"{self.name}. Erro: {msg}")


    def add_stamp_backward(self):
        g = 1/self.R
        self.Yn[self.nodeA, self.nodeA] += g
        self.Yn[self.nodeB, self.nodeB] += g
        self.Yn[self.nodeA, self.nodeB] += -g
        self.Yn[self.nodeB, self.nodeA] += -g
>>>>>>> dev
