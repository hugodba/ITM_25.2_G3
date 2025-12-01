from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from abc import ABC, abstractmethod

class Element(ABC):
    """Base class for circuit elements."""
    def __init__(self, name: str):
        self.name = name
        self.parent_circuit: Circuit | None = None

    @abstractmethod
    def add_conductance(self, G, I, x_t, deltaT, method, t):
        return G, I
    
    def update(self, x_t):
        pass  # Placeholder for future implementation

    def on_add(self):
        pass  # Placeholder for actions to perform when the element is added to a circuit

    def __str__(self):
        return f"Element(name={self.name})"
    
    def __repr__(self):
        return self.__str__()
