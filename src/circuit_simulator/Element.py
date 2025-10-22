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

    def __init__(self, splitline_netlist, Yn, In, method="backward"):
        self.name = splitline_netlist[0]   # Ex: "R1"
        self.splitline_netlist = splitline_netlist
        self.Yn = Yn                      # Matriz de admitâncias do circuito
        self.In = In                      # Vetor de correntes injetadas
        self.method = method              # Método numérico (ex: "backward")

    @staticmethod
    def create(splitline_netlist, Yn, In, method="backward", elem_type=None, **kwargs):
        """
        Cria automaticamente a instância correta do elemento com base no prefixo.
        Exemplo: "R1" -> classe Resistor.
        Args: 
            elem_type (str): "invariant", "variant" or "non_linear". Descreve o 
                tipo do elemento, para criar o elemento da netlist apenas se for 
                do mesmo tipo requisitado.   
        """

        prefix = splitline_netlist[0][0].lower()  # Ex: "r" em "R1"
        cls = Element.registry.get(prefix)
        if cls is None:
            raise ValueError(f"Tipo de elemento desconhecido: {splitline_netlist[0]}")
        
        # Retorna o elemento após executado somente se for do tipo desejado.
        # Motivo: criar os invariantes no tempo, variantes e os não lineares 
        # separadamente. 
        if (elem_type is None) or (cls.elem_type == elem_type):
            return cls(splitline_netlist, Yn, In, method, **kwargs)

    def add_stamp_backward(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_backward().")

    def add_stamp_forward(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_forward().")

    def add_stamp_trapezio(self):
        raise NotImplementedError("Subclasses devem implementar add_stamp_trapezio().")

    def add_stamp(self, method):
        if method == "backward":
            self.add_stamp_backward(self)
        elif method == "forward":
            self.add_stamp_forward(self)
        elif method == "trapezio":
            self.add_stamp_trapezio(self)

    def add_newblanklines_YnIn(self, newlines=1):
        n = len(self.Yn)
        newYn = np.zeros((n + newlines, n + newlines))
        newIn = np.zeros((n + newlines, 1))
        newYn[:n, :n] = self.Yn[:, :]
        newIn[:n] = self.In[:]
        
        self.Yn = newYn
        self.In = newIn


    def __str__(self):
        return f"Elemento genérico {self.name}"