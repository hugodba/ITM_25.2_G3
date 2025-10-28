from src.circuit_simulator.Element import Element
from numpy import ndarray


class Indutor(Element, prefix='l'):
    """Classe representando o Indutor."""

    elem_type = "variant"
    elem_name = "Indutor"
    
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
        self.i_index = self.Yn.shape[0] - 2  # Índice da variável auxiliar no vetor de tensão nodal
        self.save_info()

    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            self.L = float(splitline_netlist[3])
            self.i_initial = 0.0
            if len(splitline_netlist) == 5:
                self.i_initial = float(splitline_netlist[4][3:]) # Remove "IC="
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do indutor "
                             f"{self.name}. Erro: {msg}")

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "Valor": self.L,
                "Unidade": "H",
                "i_index": self.i_index  # Índice da variável auxiliar no vetor de tensão nodal
            }

    def add_stamp_backward(self):
        # Adiciona nova linha e uma nova coluna devido à variável auxiliar de corrente
        self.add_newblanklines_YnIn(newlines=1)

        # Adiciona a estampa na Yn
        self.Yn[self.nodeA, -1] += 1
        self.Yn[self.nodeB, -1] += -1
        self.Yn[-1, self.nodeA] += -1
        self.Yn[-1, self.nodeB] += 1
        self.Yn[-1, -1] += self.L/self.deltaT

        # Corrente no indutor caso seja o primeiro tempo
        i0 = self.i_initial
        if self.e0 is not None: # Se não for o primeiro passo de tempo.
            # Corrente no indutor no tempo anterior
            i0_index = self.Yn.shape[0] - 2
            i0 = self.e0[i0_index]

        # Adiciona a estampa da matriz In
        self.In[-1] += i0*self.L/self.deltaT