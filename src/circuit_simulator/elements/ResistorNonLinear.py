from src.circuit_simulator.Element import Element
from numpy import ndarray

class ResistorNonLinear(Element, prefix='n'):
    """Classe representando um Resistor Não Linear."""

    elem_type = "non_linear"
    elem_name = "ResistorNonLinear"

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
                "Valor": self.R_func.__name__,
                "Unidade": "Ω",
            }

    def extract_values(self, splitline_netlist):
        try:
            self.nodeA = int(splitline_netlist[1])
            self.nodeB = int(splitline_netlist[2])
            # Aqui assumimos que a função resistência é passada como uma string
            func_name = splitline_netlist[3]
            self.R_func = globals()[func_name]  # A função deve estar definida globalmente
        except Exception as msg:
            raise ValueError(f"Valores inválidos na definição do resistor não linear "
                             f"{self.name}. Erro: {msg}")


    def add_stamp_backward(self):
        # Exemplo simplificado: obter resistência a partir da função para uma tensão específica
        V_ab = self.e[self.nodeA] - self.e[self.nodeB]
        R_value = self.R_func(V_ab)
        g = 1/R_value
        self.Yn[self.nodeA, self.nodeA] += g
        self.Yn[self.nodeB, self.nodeB] += g
        self.Yn[self.nodeA, self.nodeB] += -g
        self.Yn[self.nodeB, self.nodeA] += -g
