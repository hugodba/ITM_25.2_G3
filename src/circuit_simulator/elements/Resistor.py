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