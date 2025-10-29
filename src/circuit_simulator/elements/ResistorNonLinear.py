from src.circuit_simulator.Element import Element
from numpy import ndarray

class ResistorNonLinear(Element, prefix='n'):
    """Classe representando um Resistor Não Linear."""

    elem_type = "non_linear"
    elem_name = "ResistorNonLinear"

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, elems_info: dict, method: str,
            deltaT: float, e0: ndarray
        ):
        
        super().__init__(splitline_netlist, Yn, In, elems_info, method)
        self.extract_values(splitline_netlist)
        self.deltaT = deltaT
        self.e0 = e0
        self.add_stamp(method)
        self.save_info()

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "Valor": self.R_func.__name__,
                "Unidade": "Ω",
            }

    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            self.v1 = float(splitline_netlist[3])
            self.i1 = float(splitline_netlist[4])
            self.v2 = float(splitline_netlist[5])
            self.i2 = float(splitline_netlist[6])
            self.v3 = float(splitline_netlist[7])
            self.i3 = float(splitline_netlist[8])
            self.v4 = float(splitline_netlist[9])
            self.i4 = float(splitline_netlist[10])
            
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do resistor não linear "
                             f"{self.name}. Erro: {msg}")

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "tension1": self.v1,
                "current1": self.i1,
                "tension2": self.v2,
                "current2": self.i2,
                "tension3": self.v3,
                "current3": self.i3,
                "tension4": self.v4,
                "current4": self.i4
            }

    def add_stamp_backward(self):
        # Exemplo simplificado: obter resistência a partir da função para uma tensão específica
        V_ab = self.e0[self.nodeA -1] - self.e0[self.nodeB -1]

        if V_ab > self.v3:
            G0 = (self.i4 - self.i3) / (self.v4 - self.v3)
            I0 = self.i4 - G0 * self.v4
        elif V_ab > self.v2 and V_ab <= self.v3:
            G0 = (self.i3 - self.i2) / (self.v3 - self.v2)
            I0 = self.i3 - G0 * self.v3
        else:
            G0 = (self.i2 - self.i1) / (self.v2 - self.v1)
            I0 = self.i2 - G0 * self.v2
        
        self.Yn[self.nodeA, self.nodeA] += G0
        self.Yn[self.nodeA, self.nodeB] += -G0
        self.Yn[self.nodeB, self.nodeA] += -G0
        self.Yn[self.nodeB, self.nodeB] += G0
        
        self.In[self.nodeA] += -I0
        self.In[self.nodeB] += I0
