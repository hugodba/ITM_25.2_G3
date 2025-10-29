from abc import ABC, abstractmethod

class Element(ABC):
    """Base class for circuit elements."""
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def add_conductance(self, G, I, x_t, deltaT, method):
        return G, I
    
    def update(self, x_t):
        pass  # Placeholder for future implementation
    
    def __str__(self):
       return f"Element: {self.name}"
