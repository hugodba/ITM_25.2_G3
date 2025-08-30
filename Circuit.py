class Circuit:
    """Base class for circuits."""
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def __str__(self):
        return f"Circuit with {len(self.elements)} elements."
