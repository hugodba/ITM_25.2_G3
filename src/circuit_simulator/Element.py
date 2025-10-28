import numpy as np

class Element:
    """Classe base para elementos de circuito elétrico."""

    registry = {}  # Dicionário de elementos filhos registrados

    def __init_subclass__(cls, prefix=None, **kwargs):
        """
        Método chamado automaticamente quando uma subclasse de Element é criada.
        Se a subclasse fornecer um prefixo, ela é registrada automaticamente.
        """
        super().__init_subclass__(**kwargs)
        if prefix is not None:
            Element.registry[prefix.lower()] = cls

    def __init__(self, splitline_netlist, Yn, In, elems_info, method="backward"):
        self.name = splitline_netlist[0]  # Ex: "R1"
        self.Yn, self.In = Yn, In         # Matrizes do sistema
        self.method = method              # Método numérico (ex: "backward")
        self.elems_info = elems_info      # Dicionário com as informações dos elementos

    @staticmethod
    def create(splitline_netlist, Yn, In, elems_info, method="backward", elem_type=None, **kwargs):
        """
        Cria automaticamente a instância correta do elemento com base no prefixo.
        Exemplo: "R1" -> classe Resistor.
        Args: 
            elem_type (str): "invariant", "variant" ou "non_linear". Descreve o 
                tipo do elemento, para criar o elemento da netlist apenas se for 
                do mesmo tipo requisitado.   
        """

        prefix = splitline_netlist[0][0].lower()  # Ex: "r" em "R1"
        if prefix == "v":
            if splitline_netlist[3] == "DC":
                prefix = "vdc"
            elif splitline_netlist[3] == "SIN":
                prefix = "vsin"
            elif splitline_netlist[3] == "PULSE":
                prefix = "vpulse"
            else:
                raise ValueError(f"Tipo de fonte de tensão inválido: {splitline_netlist[3]}")

        cls = Element.registry.get(prefix)
        if cls is None:
            raise ValueError(f"Tipo de elemento desconhecido: {splitline_netlist[0]}")
        
        # Retorna o elemento apenas se for do tipo desejado.
        # Motivo: criar os elementos invariantes no tempo, variantes e não lineares 
        # separadamente. 
        if (elem_type is None) or (cls.elem_type == elem_type):
            return cls(splitline_netlist, Yn, In, elems_info, method, **kwargs)

    def extract_values(self, splitline_netlist):
        raise NotImplementedError("Subclasses devem implementar extract_values().")
    
    def save_info(self):
        raise NotImplementedError("Subclasses devem implementar save_info().")

    def add_stamp_backward(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_backward().")

    def add_stamp_forward(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_forward().")

    def add_stamp_trapezio(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_trapezio().")

    def add_stamp(self, method):
        if method == "backward":
            self.add_stamp_backward()
        elif method == "forward":
            self.add_stamp_forward()
        elif method == "trapezio":
            self.add_stamp_trapezio()

    def add_newblanklines_YnIn(self,newlines=1):
        self.Yn = np.pad(self.Yn, ((0, newlines), (0, newlines)), mode='constant')
        self.In = np.pad(self.In, ((0, newlines), (0, 0)), mode='constant')

    def __str__(self):
        return f"Elemento genérico {self.name}"
