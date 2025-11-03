from src.circuit_simulator.Element import Element
from numpy import ndarray


class FonteTensaoControlTensao(Element, prefix='e'):
    """Classe representando uma fonte de tensão controlada por tensão."""

    elem_type = "invariant"
    elem_name = "Fonte de Tensão Controlada por Tensão"

    def __init__(self, 
            splitline_netlist: list, 
            Yn: ndarray, In: ndarray, elems_info: dict, method: str, **kwargs
        ):

        super().__init__(splitline_netlist, Yn, In, elems_info, method)
        self.extract_values(splitline_netlist)
        self.add_stamp(method)
        self.i_index = self.Yn.shape[0] - 2  # Índice da variável auxiliar no vetor de tensão nodal
        self.save_info()

    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            self.node_controlA = int(splitline_netlist[3])
            self.node_controlB = int(splitline_netlist[4])
            self.A = float(splitline_netlist[5])
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do resistor "
                             f"{self.name}. Erro: {msg}")

    def save_info(self):
        """Salva as informações do elemento em um dicionário."""
        if self.name not in self.elems_info:
            self.elems_info[self.name] = {
                "tipo": self.elem_name,
                "nodeA": self.nodeA,
                "nodeB": self.nodeB,
                "node_controlA": self.node_controlA,
                "node_controlB": self.node_controlB,
                "Valor": self.A,
                "Unidade": "V",
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
        self.Yn[-1, self.node_controlA] += self.A
        self.Yn[-1, self.node_controlB] += -self.A
