from src.circuit_simulator.Element import Element
from numpy import ndarray


class Capacitor(Element, prefix='c'):
    """Classe representando o Capacitor."""

    elem_type = "variant"
    elem_name = "Capacitor"

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, elems_info: dict, method: str, 
            deltaT: float, e0: ndarray, **kwargs
        ):
        super().__init__(splitline_netlist, Yn, In, elems_info, method)
        self.deltaT = deltaT
        self.e0 = e0
        self.extract_values(splitline_netlist)
        self.add_stamp(method)
        self.save_info()


    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            self.C = float(splitline_netlist[3])
            self.v_initial = 0.0
            if len(splitline_netlist) == 5:
                self.v_initial = float(splitline_netlist[4][3:]) # Remove "IC="
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do capacitor "
                             f"{self.name}. Erro: {msg}")

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "Valor": self.C,
                "Unidade": "F",
            }


    def add_stamp_backward(self):
        # Adiciona a estampa na Yn
        self.Yn[self.nodeA, self.nodeA] +=  self.C/self.deltaT
        self.Yn[self.nodeA, self.nodeB] +=  -self.C/self.deltaT
        self.Yn[self.nodeB, self.nodeA] +=  -self.C/self.deltaT
        self.Yn[self.nodeB, self.nodeB] +=  self.C/self.deltaT

        # Tensão no capacitor caso seja o primeiro tempo
        v0 = self.v_initial
        if self.e0 is not None: # Se não for o primeiro passo de tempo.
            # Tensão no capacitor no tempo anterior
            eA = eB = 0
            if self.nodeA != 0:
                eA = self.e0[self.nodeA - 1]
            if self.nodeB != 0:
                eB = self.e0[self.nodeB - 1]
            v0 = eA - eB      

        # Adiciona a estampa da matriz In
        self.In[self.nodeA] += v0*self.C/self.deltaT
        self.In[self.nodeB] += -v0*self.C/self.deltaT