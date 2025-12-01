from typing import TYPE_CHECKING
import math
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from circuit_simulator import Circuit, Element

class Mosfet(Element):
    """Class representing a MOSFET."""
    def __init__(
        self,
        name: str,
        drain_node: int,
        gate_node: int,
        source_node: int,
        type: str,
        w_variable: float,
        l_variable: float,
        lambda_variable: float,
        k_variable: float,
        vth_variable: float,
    ) -> None:
        super().__init__(name)
        self.drain_node = drain_node
        self.gate_node = gate_node
        self.source_node = source_node
        self.type = type
        self.w_variable = w_variable
        self.l_variable = l_variable
        self.lambda_variable = lambda_variable
        self.k_variable = k_variable
        self.vth_variable = vth_variable

    def add_conductance(self, G, I, x_t, deltaT, method, t):

        if method == "BE":
            d = self.drain_node
            g = self.gate_node
            s = self.source_node

            # Troca drain/source se necessário
            if self.type == "N":
                if x_t[d] < x_t[s]:
                    d = self.source_node
                    s = self.drain_node
                vgs = 2 if t == 0 else x_t[g] - x_t[s]
                vds = x_t[d] - x_t[s]

            elif self.type == "P":
                if x_t[d] > x_t[s]:
                    d = self.source_node
                    s = self.drain_node
                vgs = -2 if t == 0 else -1*(x_t[g] - x_t[s])
                vds = -1*(x_t[d] - x_t[s])

            else:
                raise ValueError("Tipo de MOSFET desconhecido.")

            # Regiões de operação
            constant = self.k_variable * (self.w_variable / self.l_variable)

            if vgs > self.vth_variable:
                    # Saturação
                vds = x_t[d] - x_t[s]

                if vds >= vgs - self.vth_variable:
                    gm =  constant * (2 * (vgs - self.vth_variable) * (1 + self.lambda_variable * vds))
                    id = constant * (vgs - self.vth_variable)**2 * (1 + self.lambda_variable * vds)
                    gds = constant * (vgs - self.vth_variable)**2 * self.lambda_variable
                    # Triodo
                else:
                    id = constant * (2*(vgs - self.vth_variable) * vds -  vds**2 ) * (1 + self.lambda_variable * vds)
                    gm = constant * (2 * vds * (1 + self.lambda_variable * vds))
                    gds = constant * (2 * (vgs - self.vth_variable) - 2 * vds + 4 * self.lambda_variable*(vgs - self.vth_variable) - 3 * self.lambda_variable*vds**2)

                id = id - gm*vgs - gds*vds

            else:
                # Corte
                gm = gds = id =0

            G[d,d] += gds
            G[d,s] += -gds
            G[s,d] += -gds
            G[s,s] += gds

            G[d,g] += gm
            G[d,s] += -gm
            G[s,g] += -gm
            G[s,s] += gm
            
            I[d] += -id
            I[s] += id

            return G, I

        elif method == 'FE':
            print("Forward Euler method not implemented for MOSFET yet.")
            return G, I

        elif method == 'TRAP':
            print("Trapezoidal method not implemented for MOSFET yet.")
            return G, I

        else:
            raise ValueError("Método de análise desconhecido.")
       
    