from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from abc import ABC, abstractmethod

class Element(ABC):
    """Base class for circuit elements."""
    def __init__(self, parent_circuit: "Circuit", name: str):
        self.name = name
        self.parent_circuit = parent_circuit
        
    @abstractmethod
    def add_conductance(self, G, I, x_t, deltaT, method):
        return G, I
    
    def update(self, x_t):
        pass  # Placeholder for future implementation

    def __str__(self):
        return f"Element(name={self.name})"
    
    def __repr__(self):
        return self.__str__()
