from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from circuit_simulator.Circuit import Circuit

from abc import ABC, abstractmethod

class Element(ABC):
    """Base class for circuit elements."""

    def __init__(self, name: str) -> None:
        '''Initialize the element with a name.'''
        self.name = name
        self.parent_circuit: Circuit | None = None

    @abstractmethod
    def add_conductance(self, G, I, x_t, deltaT, method, t) -> tuple:
        """Add the element's contribution to the conductance matrix G and current vector I."""
        return G, I
    
    def update(self, x_t) -> None:
        """Update the element state based on the current solution vector x_t."""
        pass

    def on_add(self) -> None:
        """Hook method called when the element is added to a circuit."""
        pass

    @abstractmethod
    def to_netlist(self) -> str:
        """Return a string representation of the element in netlist format."""
        pass

    def __str__(self):
        return f"Element(name={self.name})"
    
    def __repr__(self):
        return self.__str__()
    
    
