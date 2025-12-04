from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element
import numpy as np

class Diode(Element):
    """Diode using simplified exponential model with linearization."""
    
    IS = 3.7751345e-14   # saturation current
    VT = 25e-3           # thermal voltage
    
    def __init__(self, name: str, node1: int, node2: int):
        super().__init__(name)
        self.node1 = node1
        self.node2 = node2

    def add_conductance(self, G, I, x_t, deltaT, method, t):

        if method == "BE":
            # ---- 1. calcula v_ab a partir do vetor de tensões atual ----
            v_ab = x_t[self.node1] - x_t[self.node2]

            # saturação a 0.9 V como no enunciado
            if v_ab > 0.9:
                v_ab = 0.9

            # ---- 2. calcula G0 e ID como na imagem ----
            exp_term = np.exp(v_ab / self.VT)

            G0 = (self.IS * exp_term) / self.VT
            ID = (self.IS * (exp_term - 1)) - (G0 * v_ab)

            # ---- 3. Estampa na matriz de condutância ----
            G[self.node1, self.node1] += G0
            G[self.node1, self.node2] += -G0
            G[self.node2, self.node1] += -G0
            G[self.node2, self.node2] += G0

            # ---- 4. Estampa no vetor de correntes ----
            I[self.node1] += -ID   # corrente sai do nó a
            I[self.node2] += ID   # corrente entra no nó b

            return G, I
        
        elif method == 'FE':
            print("Forward Euler method not implemented for OperationalAmplifier yet.")
            return G, I

        elif method == 'TRAP':
            print("Trapezoidal method not implemented for OperationalAmplifier yet.")
            return G, I

        else:
            raise ValueError("Método de análise desconhecido.")
    
    def to_netlist(self):
        return f"{self.name} {self.node1} {self.node2}"
